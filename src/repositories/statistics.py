from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.db.session import engine
from src.exceptions.base import ObjectNotFoundException
from src.mappers.mappers import PopularBookMapper, TopAuthorMapper, ReviewStatsMapper
from src.models.stat_views import PopularBook, TopAuthor, ReviewStats
from src.repositories.base import BaseRepository


class PopularBookRepository(BaseRepository):
    model = PopularBook
    mapper = PopularBookMapper

    async def get_all(self):
        query = select(self.model)
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        model = result.scalars().all()
        return [self.mapper.map_to_domain_entity(obj) for obj in model]


class TopAuthorRepository(BaseRepository):
    model = TopAuthor
    mapper = TopAuthorMapper

    async def get_all(self):
        query = select(self.model)
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        model = result.scalars().all()
        return [self.mapper.map_to_domain_entity(obj) for obj in model]


class ReviewStatsRepository(BaseRepository):
    model = ReviewStats
    mapper = ReviewStatsMapper

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
            return self.mapper.map_to_domain_entity(model) if model else None
        except NoResultFound:
            raise ObjectNotFoundException
