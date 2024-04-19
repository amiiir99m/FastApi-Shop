from fastapi import APIRouter, Body, Depends
from db.engine import get_db
from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession
from operations.images import ImageOperation
from schema.jwt import JWTPayload
from utils.jwt import JWTHandler
from schema.input import ImageInput, ImageUpdateInput
import os
import uuid
from uuid import UUID

router = APIRouter()

    

@router.post("/create_image/")
async def create_image(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    data = Depends(ImageInput),
    token_data : JWTPayload = Depends(JWTHandler.verify_token),
):
    
    upload_folder = "C:/Users/user/Desktop/FastApi-shop/static"

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    file_uuid = uuid.uuid4()
    file_name = f"{file_uuid}.{str(data.file.filename).split('.')[-1]}"
    file_path = os.path.join(upload_folder, file_name)
    contents = await data.file.read()  
    with open(file_path, "wb") as buffer:
        buffer.write(contents)   
    image_url = "/static/" + file_name

    p = await ImageOperation(db_session).create(
        user=token_data.username, image = image_url, product_title=data.product_title
    ) 
    return p


@router.put('/')
async def update_image(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    data = Depends(ImageUpdateInput),   
    token_data : JWTPayload = Depends(JWTHandler.verify_token),
):
    
    upload_folder = "C:/Users/user/Desktop/FastApi-shop/static"

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    file_uuid = uuid.uuid4()
    file_name = f"{file_uuid}.{str(data.file.filename).split('.')[-1]}"
    file_path = os.path.join(upload_folder, file_name)
    contents = await data.file.read()  
    with open(file_path, "wb") as buffer:
        buffer.write(contents)   
    image_url = "/static/" + file_name

    product = await ImageOperation(db_session).update_image(
        user = token_data.username, image = image_url, image_id = data.image_id)
    return product


@router.delete('/')
async def delete_image(
    db_session: Annotated[AsyncSession, Depends(get_db)],       
    image_id: List[UUID] = Body(),
    token_data : JWTPayload = Depends(JWTHandler.verify_token),
):
    for x in image_id:
        await ImageOperation(db_session).delete(user=token_data.username, image_id=x)
