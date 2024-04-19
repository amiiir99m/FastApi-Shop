import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from exceptions import UserAlreadyExists, UsernameOrPasswordIncorrect, UserNotFound
from schema.jwt import JWTResponsePayload
from schema.output import UserOutput
from utils.jwt import JWTHandler
from utils.secret import password_manager


class UsersOperation:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create(self, username:str, password:str, role:str) -> UserOutput:
        user_pwd = password_manager.hash(password)
        user = User(password=user_pwd, username=username, role=role)

        async with self.db_session as session:
            try:
                session.add(user)
                await session.commit()
            except IntegrityError:
                raise UserAlreadyExists

        return UserOutput(username=user.username, id=user.id)
    
    async def get_user_by_username(self, username:str) -> UserOutput:
        query = sa.select(User).where(User.username == username)

        async with self.db_session as session:
            user_data = await session.scalar(query)

            if user_data is None:
                raise UserNotFound
            
            return UserOutput(username=user_data.username, id=user_data.id)
        
    async def update_username(self, old_username: str, new_username: str) -> UserOutput:
        query = sa.select(User).where(User.username == old_username)
        update_query = sa.update(User).where(User.username == old_username).values(username = new_username)

        async with self.db_session as session:
            user_data = await session.scalar(query)

            if user_data is None:
                raise UserNotFound
            
            await session.execute(update_query)
            await session.commit()
            
            user_data.username = new_username
            return UserOutput(username=user_data.username, id=user_data.id)

    async def user_delete_account(self, username:str) -> None:
        delete_query = sa.delete(User).where(User.username == username) #type: ignore

        async with self.db_session as session:
            await session.execute(delete_query)
            await session.commit()

    async def login(self, username:str, password:str) -> JWTResponsePayload:
        query = sa.select(User).where(User.username==username)

        async with self.db_session as session:
            user = await session.scalar(query)

            if user is None:
                raise UsernameOrPasswordIncorrect
        
        if not password_manager.verify(password, user.password):
            raise UsernameOrPasswordIncorrect
        
        return JWTHandler.generate(username)
