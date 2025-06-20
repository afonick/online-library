from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.db.session import engine
from src.exceptions.base import LibraryException
from src.exceptions.book import BookNotFoundException
from src.exceptions.review import RatingErrorException, ReviewNotFoundException
from src.mappers.mappers import ReviewMapper
from src.models import Book
from src.repositories.base import BaseRepository
from src.models.review import Review


class ReviewRepository(BaseRepository):
    model = Review
    mapper = ReviewMapper

    async def get_all(self, limit, offset):
        query = select(self.model)
        query = query.limit(limit).offset(offset)
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        model = result.scalars().all()
        return [self.mapper.map_to_domain_entity(obj) for obj in model]

    async def get_book_reviews(self, book_id):
        query_book = await self.session.execute(select(Book).filter_by(id=book_id))
        book = query_book.scalars().first()
        if not book:
            raise BookNotFoundException
        query = select(self.model).where(self.model.book_id == book_id)
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        model = result.scalars().all()
        return [self.mapper.map_to_domain_entity(obj) for obj in model]

    async def add(self, data: BaseModel, **filter_by):
        insert_stmt = insert(self.model).values(**data.model_dump(), **filter_by).returning(self.model)

        try:
            result = await self.session.execute(insert_stmt)
            model = result.scalars().one()
            return self.mapper.map_to_domain_entity(model)
        except IntegrityError:
            raise LibraryException

    async def update(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        if data.rating < 1 or data.rating > 5:
            raise RatingErrorException
        update_stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=exclude_unset))
        await self.session.execute(update_stmt)

    async def delete(self, *args, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by).filter(*args)
        await self.session.execute(delete_stmt)

    async def check_book(self, book_id):
        try:
            book_query = select(Book).filter_by(id=book_id)
            book_result = await self.session.execute(book_query)
            book_result.scalar_one()
        except NoResultFound:
            raise BookNotFoundException

    async def check_review_book(self, review_id, book_id):
        try:
            review_query = select(self.model).filter_by(id=review_id, book_id=book_id)
            review_result = await self.session.execute(review_query)
            review_result.scalar_one()
        except NoResultFound:
            raise ReviewNotFoundException
