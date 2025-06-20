from pydantic import BaseModel
from sqlalchemy import select, insert, delete
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.functions import coalesce

from src.db.session import engine
from src.exceptions.base import LibraryException
from src.exceptions.book import BookNotFoundException
from src.exceptions.favorite import FavoriteBookNotFoundException, FavoriteBookNotUniqueException
from src.mappers.mappers import FavoriteMapper
from src.models import Book, Favorite
from src.models.stat_views import BookRatingStats
from src.repositories.base import BaseRepository


class FavoriteRepository(BaseRepository):
    model = Favorite
    mapper = FavoriteMapper

    async def get_favorites(self, user_id, limit, offset):
        query = (
            select(
                self.model,
                Book,
                coalesce(BookRatingStats.avg_rating, 0).label("avg_rating"),
                coalesce(BookRatingStats.review_count, 0).label("review_count"),
            )
            .join(Book, Favorite.book_id == Book.id)
            .outerjoin(BookRatingStats, Book.id == BookRatingStats.book_id)
            .where(Favorite.user_id == user_id)
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        rows = result.all()

        favorites = []
        for fav, book, avg_rating, review_count in rows:
            book.avg_rating = avg_rating
            book.review_count = review_count
            fav.book = book  # чтобы joinedload не был нужен
            favorites.append(self.mapper.map_to_domain_entity(fav))

        return favorites

    async def add(self, data: BaseModel, **filter_by):
        insert_stmt = insert(self.model).values(**data.model_dump(), **filter_by).returning(self.model)

        try:
            result = await self.session.execute(insert_stmt)
            model = result.scalars().one()
            query_relation = select(self.model).options(joinedload(self.model.book)).where(self.model.id == model.id)
            result_relation = await self.session.execute(query_relation)
            model_relation = result_relation.scalar_one()
            return self.mapper.map_to_domain_entity(model_relation)
        except IntegrityError:
            raise LibraryException

    async def delete(self, *args, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by).filter(*args)
        print(delete_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute(delete_stmt)

    async def check_book(self, book_id):
        try:
            book_query = select(Book).filter_by(id=book_id)
            book_result = await self.session.execute(book_query)
            book_result.scalar_one()
        except NoResultFound:
            raise BookNotFoundException

    async def check_favorite_book(self, book_id, user_id):
        try:
            favorite_query = select(self.model).filter_by(user_id=user_id, book_id=book_id)
            favorite_result = await self.session.execute(favorite_query)
            favorite_result.scalar_one()
        except NoResultFound:
            raise FavoriteBookNotFoundException

    async def check_unique_favorite_book(self, book_id, user_id):
        favorite_query = select(self.model).filter_by(user_id=user_id, book_id=book_id)
        favorite_result = await self.session.execute(favorite_query)
        if favorite_result.scalar_one_or_none():
            raise FavoriteBookNotUniqueException
