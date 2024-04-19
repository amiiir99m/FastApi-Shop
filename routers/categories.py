from fastapi import APIRouter, Body, Depends
from db.engine import get_db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from operations.categories import CategoryOperation
from schema.jwt import JWTPayload
from utils.jwt import JWTHandler


router = APIRouter()


@router.post("/create_category/")
async def create_category(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    title:str = Body(),
    token_data : JWTPayload = Depends(JWTHandler.verify_token),
):
    category = await CategoryOperation(db_session).create(title=title, username=token_data.username)
    return category


@router.put("/")
async def update_category(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    old_title:str,
    new_title:str,
    token_data : JWTPayload = Depends(JWTHandler.verify_token),
):
    user = await CategoryOperation(db_session).update(
        old_title=old_title, new_title=new_title, username=token_data.username)

    return user


@router.delete("/")
async def delete_category(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    title:str,
    token_data : JWTPayload = Depends(JWTHandler.verify_token),


):
    await CategoryOperation(db_session).delete(title=title, username=token_data.username)


@router.get('/{title}/')
async def get_category(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    title: str
):
    category = await CategoryOperation(db_session).get_category_by_title(title=title)

    return category


@router.get('/')
async def get_all_categories(
    db_session: Annotated[AsyncSession, Depends(get_db)],
):
    categories = await CategoryOperation(db_session).get_all_categories()
    return categories