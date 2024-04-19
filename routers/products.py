from fastapi import APIRouter, Body, Depends
from db.engine import get_db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from operations.products import ProductOperation
from schema.jwt import JWTPayload
from utils.jwt import JWTHandler
from schema.input import ProductInput
from typing import Optional


router = APIRouter()


@router.post("/create_product/")
async def create_product(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    data: ProductInput,
    token_data : JWTPayload = Depends(JWTHandler.verify_token),
):
    product = await ProductOperation(db_session).create(
        title=data.title, description=data.description, price=data.price,
        user=token_data.username, category=data.category, in_stock=data.in_stock) 
    return product


@router.get('/')
async def get_all_products(
    db_session: Annotated[AsyncSession, Depends(get_db)],
):
    products = await ProductOperation(db_session).get_all_products()
    return products


@router.get('/{title}')
async def get_product_by_title(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    title: str
):
    product = await ProductOperation(db_session).get_product_by_title(title=title)
    return product


@router.put('/')
async def update_prouct(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    old_title: str = Body(),
    new_title: str = Body(None),
    new_price: Optional[int] = Body(None),
    in_stock: Optional[bool] = Body(None),
    token_data : JWTPayload = Depends(JWTHandler.verify_token),
):
    product = await ProductOperation(db_session).update_product(
        old_title=old_title, new_title=new_title,
        user=token_data.username, new_price=new_price, in_stock=in_stock
        )
    return product


@router.delete('/')
async def delete_product(
    db_session: Annotated[AsyncSession, Depends(get_db)],       
    title: str = Body(),
    token_data : JWTPayload = Depends(JWTHandler.verify_token),
):
    await ProductOperation(db_session).delete(user=token_data.username, title=title)

