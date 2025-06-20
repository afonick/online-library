from pydantic import EmailStr, BaseModel
from sqlalchemy import select, insert, update
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.db.session import engine
from src.exceptions.user import ExistsUserException, IsNotActiveUserException, UserNotFoundException
from src.mappers.mappers import UserMapper, UserLoginMapper, UserCodeMapper
from src.repositories.base import BaseRepository
from src.models import User


class UserRepository(BaseRepository):
    model = User
    mapper = UserMapper

    async def get_user_for_login(self, username: str, email: EmailStr):
        query = select(self.model).filter_by(username=username, email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        if not model.is_active:
            raise IsNotActiveUserException
        return UserLoginMapper.map_to_domain_entity(model)

    async def add_user(self, data: BaseModel, **filter_by):
        insert_stmt = insert(self.model).values(**data.model_dump(), **filter_by).returning(self.model)
        try:
            result = await self.session.execute(insert_stmt)
            model = result.scalars().one()
            return self.mapper.map_to_domain_entity(model)
        except IntegrityError:
            raise ExistsUserException

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
            return self.mapper.map_to_domain_entity(model) if model else None
        except NoResultFound:
            raise UserNotFoundException

    async def get_user(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
            return UserCodeMapper.map_to_domain_entity(model) if model else None
        except NoResultFound:
            raise UserNotFoundException

    async def activate(self, **filter_by) -> None:
        is_active = filter_by.pop('is_active')
        update_stmt = update(self.model).filter_by(**filter_by).values(is_active=is_active, code="applied")
        print(update_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute(update_stmt)
