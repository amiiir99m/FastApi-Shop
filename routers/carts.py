from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.engine import get_db
from operations.carts import CartOperation
from schema.jwt import JWTPayload
from utils.jwt import JWTHandler

router = APIRouter()


@router.post("/create_cart/")
async def add_to_cart(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    product_title:str = Body(),
    quantity: int = Body(),
    token_data : JWTPayload = Depends(JWTHandler.verify_token),
):
    cart_item = await CartOperation(db_session).add_item_to_cart(
        product_title=product_title, quantity=quantity, user=token_data.username
    )
    return cart_item


@router.put("/shopping_is_done")
async def close_cart(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    token_data : JWTPayload = Depends(JWTHandler.verify_token),    
):
    done = await CartOperation(db_session).finish_shoping(user=token_data.username)
    return done


@router.put("/update_cart_items")
async def update_cart_item(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    token_data : JWTPayload = Depends(JWTHandler.verify_token),    
    id:UUID = Body(),
    quantity: int = Body()
):
    done = await CartOperation(db_session).update_cart_item(id=id, user=token_data.username, quantity=quantity)
    return done


@router.get('/get_carts_by_user')
async def get_carts_by_user(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    token_data : JWTPayload = Depends(JWTHandler.verify_token),   
):
    carts = await CartOperation(db_session).get_cart_by_user(user=token_data.username)
    return carts


@router.get('/get_all_carts')
async def get_all_carts(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    token_data : JWTPayload = Depends(JWTHandler.verify_token),   
):
    carts = await CartOperation(db_session).get_all_carts(user=token_data.username)
    return carts