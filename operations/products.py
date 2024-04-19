from typing import Any

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Image, Product, User
from exceptions import (
    AccessDenied,
    CategoryAlreadyExists,
    ProductNotFound,
)

from schema.input import ProductInput



class ProductOperation:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create(
            self, title:str, description:str, price:int, user:str, in_stock:bool, category:str,
            ) -> ProductInput:
        product = Product(
            title=title, description=description, price=price,
            user=user, in_stock=in_stock, category=category
            ) 
        query = sa.select(User).where(User.username == user, User.role == "admin")

        async with self.db_session as session:
            user_data = await session.scalar(query)

            if user_data is None:
                raise AccessDenied
            
            try:
                session.add(product)
                await session.commit()
            except IntegrityError:
                raise CategoryAlreadyExists

        return ProductInput(
            title=product.title, description=product.description,
            price=product.price, category=product.category,
            )
    
    async def get_all_products(self):
        query = sa.select(
            Product, Image
            ).select_from(Product).outerjoin(Image)

        async with self.db_session as session:
            products_data = await session.execute(query)
            products_datas = [dict(row._mapping.items()) for row in products_data.fetchall()]
            product_details = {}

            for item in products_datas:
                product_id = item["Product"].id
                product_info = item["Product"]
                image_info = item["Image"]

                if product_id not in product_details:
                    product_details[product_id] = {
                        "Product": product_info,
                        "Images": []
                    }

                if image_info:
                    product_details[product_id]["Images"].append(image_info.image)

            result = list(product_details.values())

            return result
    
    async def get_product_by_title(self, title:str) -> Any:
        query = sa.select(Product).where(Product.title == title)
        image_query= sa.select(Image).where(Image.product_title == title)

        async with self.db_session as session:
            product_data = await session.scalar(query)
            image_data = await session.execute(image_query)
            image_data_s=[image for image, in image_data]

            return [product_data, image_data_s]
        
    async def update_product(self, old_title:str, user:str, new_title:str|None,
                             new_price:int|None, in_stock:bool|None):
        query = sa.select(Product).where(Product.title == old_title)
        user_query = sa.select(User).where(User.username == user, User.role == "admin")
        update_values = {} 
        if new_title is not None:
            update_values['title'] = new_title
        if new_price is not None:
            update_values['price'] = new_price #type:ignore
        if in_stock is not None:
            update_values['in_stock'] = in_stock #type:ignore
        
        #you can add everything you want here just like that 

        update_query = sa.update(Product).where(Product.title == old_title).values(**update_values)
        
        
        async with self.db_session as session:
            user_data = await session.scalar(user_query)
            if user_data is None:
                raise AccessDenied
            product_data = await session.scalar(query)
            if product_data is None:
                raise ProductNotFound
            await session.execute(update_query)
            await session.commit()
            return product_data
            
    async def delete(self, user:str, title:str) -> None:
        query = sa.select(Product).where(Product.title == title)
        user_query = sa.select(User).where(User.username == user, User.role == "admin")
        delete_query = sa.delete(Product).where(Product.title == title) #type: ignore

        async with self.db_session as session:
            product_data = await session.scalar(query)
            if product_data is None:
                raise ProductNotFound
            user_data = await session.scalar(user_query)
            if user_data is None:
                raise AccessDenied
            
            await session.execute(delete_query)
            await session.commit()




