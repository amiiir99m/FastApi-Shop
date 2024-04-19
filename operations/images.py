from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Image, Product, User
from exceptions import (
    AccessDenied,
    CategoryAlreadyExists,
    ImageNotFound,
    ProductNotFound,
)
from schema.output import ImageOutput


class ImageOperation:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create(
            self, image: str, product_title:str, user:str) -> ImageOutput:
        
        p = Image(image=image, product_title=product_title) 
        query = sa.select(User).where(User.username == user, User.role == "admin")
        query_1 = sa.select(Product).where(Product.title == product_title)

        async with self.db_session as session:
            user_data = await session.scalar(query)
            product_data = await  session.scalar(query_1)

            if user_data is None:
                raise AccessDenied
            
            if product_data is None:
                raise ProductNotFound
            
            try:
                session.add(p)
                await session.commit()
            except IntegrityError:
                raise CategoryAlreadyExists

        return ImageOutput(product_title=p.product_title, image=p.image)

    async def update_image(self, user:str, image_id:UUID, image:str|None):
        query = sa.select(Image).where(Image.id == image_id)
        user_query = sa.select(User).where(User.username == user, User.role == "admin")
        update_values = {}
        if image is not None:
            update_values['image'] = image

        update_query = sa.update(Image).where(Image.id == image_id).values(**update_values)

        async with self.db_session as session:
            user_data = await session.scalar(user_query)
            if user_data is None:
                raise AccessDenied
            image_data = await session.scalar(query)
            if image_data is None:
                raise ImageNotFound
            await session.execute(update_query)
            await session.commit()
            return image_data
        
    async def delete(self, user:str, image_id:UUID) -> None:
        query = sa.select(Image).where(Image.id == image_id)
        user_query = sa.select(User).where(User.username == user, User.role == "admin")
        delete_query = sa.delete(Image).where(Image.id == image_id) #type: ignore

        async with self.db_session as session:
            image_data = await session.scalar(query)
            if image_data is None:
                raise ImageNotFound
            user_data = await session.scalar(user_query)
            if user_data is None:
                raise AccessDenied
            
            await session.execute(delete_query)
            await session.commit()
