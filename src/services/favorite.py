from src.exceptions.base import LibraryException
from src.exceptions.book import BookNotFoundException
from src.schemas.favorite import FavoriteSchemaPost
from src.services.base import BaseService


class FavoriteService(BaseService):

    async def check_book(self, book_id: int):
        await self.db.favorite.check_book(book_id)

    async def check_favorite_book(self, book_id: int, user_id: int):
        await self.db.favorite.check_favorite_book(book_id, user_id)

    async def check_unique_favorite_book(self, book_id: int, user_id: int):
        await self.db.favorite.check_unique_favorite_book(book_id, user_id)

    async def get_favorites(self, pagination, user_id):
        page = pagination.page
        per_page = pagination.per_page
        return await self.db.favorite.get_favorites(
            user_id,
            limit=per_page,
            offset=(page - 1) * per_page
        )

    async def post_favorite(self, favorite_data: FavoriteSchemaPost):
        try:
            favorite = await self.db.favorite.add(favorite_data)
        except LibraryException:
            raise BookNotFoundException
        await self.db.commit()
        return favorite

    async def delete_favorite(self, book_id: int, user_id: int):
        await self.db.favorite.delete(book_id=book_id, user_id=user_id)
        await self.db.commit()
