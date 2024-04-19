import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Category, User
from exceptions import (
    AccessDenied,
    CategoryAlreadyExists,
    CategoryNotFound)
from schema.output import CategoryOutput


class CategoryOperation:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create(self, title:str, username:str) -> Category:
        category = Category(title=title)
        query = sa.select(User).where(User.username == username, User.role == "admin")

        async with self.db_session as session:
            user_data = await session.scalar(query)

            if user_data is None:
                raise AccessDenied
            
            try:
                session.add(category)
                await session.commit()
            except IntegrityError:
                raise CategoryAlreadyExists

        return Category(title=category.title, id=category.id)

    async def update(self, username:str, old_title: str, new_title: str) -> Category:
        user_query = sa.select(User).where(User.username == username, User.role == "admin")
        query = sa.select(Category).where(Category.title == old_title)
        update_query = sa.update(Category).where(Category.title == old_title).values(title = new_title)

        async with self.db_session as session:
            user_query = await session.scalar(user_query)
            data = await session.scalar(query)

            if user_query is None:
                raise AccessDenied

            if data is None:
                raise CategoryNotFound
            
            await session.execute(update_query)
            await session.commit()
            
            return data

    async def delete(self, username:str, title:str) -> None:
        query = sa.select(User).where(User.username == username, User.role == "admin")
        delete_query = sa.delete(Category).where(Category.title == title) #type: ignore

        async with self.db_session as session:
            user_data = await session.scalar(query)

            if user_data is None:
                raise AccessDenied

            await session.execute(delete_query)
            await session.commit()

    async def get_category_by_title(self, title:str) -> CategoryOutput:
        query = sa.select(Category).where(Category.title == title)

        async with self.db_session as session:
            category_data = await session.scalar(query)

            if category_data is None:
                raise CategoryNotFound
            
            return CategoryOutput(title = category_data.title, id=category_data.id)
        
    async def get_all_categories(self) -> list[CategoryOutput]:
        query = sa.select(Category)

        async with self.db_session as session:
            categories_data = await session.execute(query)
            data = [category for category, in categories_data]

            return data

