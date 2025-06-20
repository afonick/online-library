from pydantic import BaseModel
from sqlalchemy import select, insert, and_, func
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import joinedload

from src.db.session import engine
from src.exceptions.base import LibraryException, ObjectNotFoundException
from src.mappers.mappers import BookMapper
from src.models import User
from src.models.stat_views import BookRatingStats
from src.repositories.base import BaseRepository
from src.models.book import Book


class BookRepository(BaseRepository):
    model = Book
    mapper = BookMapper

    async def get_all(self, avg_rating, review_count, title, description, limit, offset):
        query = (
            select(
                self.model,
                func.coalesce(BookRatingStats.avg_rating, 0),
                func.coalesce(BookRatingStats.review_count, 0)
            )
            .join(BookRatingStats, Book.id == BookRatingStats.book_id, isouter=True)
            .join(User, Book.author_id == User.id)
        )
        query = query.limit(limit).offset(offset)
        filters = []

        if avg_rating is not None:
            filters.append(BookRatingStats.avg_rating >= avg_rating)

        if review_count is not None:
            filters.append(BookRatingStats.review_count >= review_count)

        if title:
            filters.append(Book.title.icontains(title))

        if description:
            filters.append(Book.description.icontains(description))

        if filters:
            query = query.where(and_(*filters))
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        rows = result.all()

        books = []
        for book, avg_rating, review_count in rows:
            book_dto = self.mapper.map_to_domain_entity(book)
            book_dto.avg_rating = avg_rating
            book_dto.review_count = review_count
            books.append(book_dto)

        return books

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by).options(joinedload(self.model.author))
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
            return self.mapper.map_to_domain_entity(model) if model else None
        except NoResultFound:
            raise ObjectNotFoundException

    async def add(self, data: BaseModel, **filter_by):
        insert_stmt = insert(self.model).values(**data.model_dump(), **filter_by).returning(self.model)

        try:
            result = await self.session.execute(insert_stmt)
            model = result.scalar_one()
            query_relation = select(self.model).options(joinedload(self.model.author)).where(self.model.id == model.id)
            result_relation = await self.session.execute(query_relation)
            model_relation = result_relation.scalar_one()
            return self.mapper.map_to_domain_entity(model_relation)
        except IntegrityError:
            raise LibraryException
