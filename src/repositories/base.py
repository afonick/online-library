from sqlalchemy import select, insert, update, delete, func
from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound, IntegrityError

from src.exceptions.base import LibraryException, ObjectUniqueException, ObjectNotFoundException
from src.mappers.base import DataMapper
from src.models import User


class BaseRepository:
    model = None
    schema: BaseModel = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        model = result.scalars().all()
        return [self.mapper.map_to_domain_entity(obj) for obj in model]

    async def get_all_with_filter(self, *args, **filter_by):
        query = select(self.model).filter_by(**filter_by).filter(*args).order_by(self.model.id)
        result = await self.session.execute(query)
        model = result.scalars().all()
        return [self.mapper.map_to_domain_entity(obj) for obj in model]

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
            return self.mapper.map_to_domain_entity(model) if model else None
        except NoResultFound:
            raise ObjectNotFoundException

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        return self.mapper.map_to_domain_entity(model) if model else None

    async def add(self, data: BaseModel, **filter_by):
        insert_stmt = insert(self.model).values(**data.model_dump(), **filter_by).returning(self.model)

        try:
            result = await self.session.execute(insert_stmt)
            model = result.scalars().one()
            return self.mapper.map_to_domain_entity(model)
        except IntegrityError:
            raise LibraryException

    async def add_multiple(self, data: list[BaseModel]):
        insert_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(insert_stmt)

    async def update(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise LibraryException
        update_stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=exclude_unset))
        await self.session.execute(update_stmt)

    async def delete(self, *args, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by).filter(*args)
        await self.session.execute(delete_stmt)

    async def check_unique(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        if result.scalars().first():
            raise ObjectUniqueException

    async def get_count_with_filter(self, *args, **filter_by):
        query = select(func.count()).select_from(self.model).filter_by(**filter_by).filter(*args)
        result = await self.session.execute(query)
        count = result.scalar_one()
        return count

    async def check_author(self, auth_user_id, **filter_by):
        user_query = select(User).filter_by(id=auth_user_id)
        user_result = await self.session.execute(user_query)
        user = user_result.scalar_one()
        if user.role.value != "admin":
            book_query = select(self.model).filter_by(**filter_by)
            book_result = await self.session.execute(book_query)
            if not book_result.scalars().first():
                raise ObjectNotFoundException
