from collections import defaultdict
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from db.models import Cart, CartItem, User
from exceptions import AccessDenied


class CartOperation:
    def __init__(self, db_session:AsyncSession) -> None:
        self.db_session = db_session
    
    async def add_item_to_cart(
            self, product_title:str, quantity:int, user:str
    ):
        cart_query = sa.select(Cart).where(Cart.user == user, Cart.complete == False)
        create_cart= Cart(user=user)
        
        async with self.db_session as session:
            cart_data = await session.scalar(cart_query)
            if cart_data is None:
                session.add(create_cart)
                await session.commit()
                new_cart_data = await session.scalar(cart_query)
                if new_cart_data is not None:
                    add_item = CartItem(product=product_title, cart=new_cart_data.id, quantity=quantity)
                session.add(add_item)
                await session.commit()
            else:
                add_item= CartItem(product=product_title, cart=cart_data.id, quantity=quantity)
                session.add(add_item)
                await session.commit()
                
            return "done"

    async def finish_shoping(
            self, user:str
    ):
        update_query = sa.update(Cart).where(Cart.user == user, Cart.complete == False).values(complete = True)
        
        async with self.db_session as session:
            await session.execute(update_query)
            await session.commit()
            
            return "done"
        
    async def update_cart_item(
            self, user:str, id:UUID, quantity:int
    ):
        update_query = sa.update(CartItem).where(CartItem.id == id).values(quantity = quantity)
        delete_query = sa.delete(CartItem).where(CartItem.id==id)
        
        async with self.db_session as session:
            if quantity<=0:
                await session.execute(delete_query)
                await session.commit()

            await session.execute(update_query)
            await session.commit()
            return "done"
        
    async def get_cart_by_user(self, user:str):
        query = select(
            CartItem.product, Cart.id, CartItem.quantity
            ).select_from(User).join(Cart).join(CartItem).where(User.username == user)

        async with self.db_session as session:
            cart_data = await session.execute(query)
            cart_datas = [dict(row._mapping.items()) for row in cart_data.fetchall()]

            grouped_data = defaultdict(list)
            for item in cart_datas:
                grouped_data[item["id"]].append({"product": item["product"], "quantity": item["quantity"]})

            result = [{"id": key, "details": value} for key, value in grouped_data.items()]

            
            return result
    
    async def get_all_carts(self, user:str):
        user_query = sa.select(User).where(User.username == user, User.role == "admin")
            
        async with self.db_session as session:
            user_data = await session.scalar(user_query)
            query = select(
                CartItem.product, Cart.id, Cart.user, CartItem.quantity
                ).select_from(User).join(Cart).join(CartItem)
            if user_data is None:
                raise AccessDenied
            
            cart_data = await session.execute(query)
            cart_datas = [dict(row._mapping.items()) for row in cart_data.fetchall()]

            grouped_data = defaultdict(list)
            for item in cart_datas:
                grouped_data[item["id"], item["user"]].append(
                    {"product": item["product"], "quantity": item["quantity"]})

            result = [{"cart": key, "details": value} for key, value in grouped_data.items()]
            
            return result
