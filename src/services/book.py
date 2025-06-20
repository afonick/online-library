from src.api.utils.file import upload_file
from src.schemas.book import BookSchemaRequest, BookSchemaPost, BookSchemaPatch
from src.services.base import BaseService


class BookService(BaseService):

    @staticmethod
    async def upload_document(file, filename):
        return await upload_file(file, filename, "document")

    async def get_all(self, pagination, avg_rating, review_count, title, description):
        page = pagination.page
        per_page = pagination.per_page
        return await self.db.book.get_all(avg_rating, review_count, title, description, limit=per_page,
                                          offset=(page - 1) * per_page)

    async def check_unique(self, title: str):
        await self.db.book.check_unique(title=title)

    async def check_author(self, auth_user_id: int, book_id: int):
        await self.db.book.check_author(auth_user_id, author_id=auth_user_id, id=book_id)

    async def get_book(self, book_id: int):
        return await self.db.book.get_one(id=book_id)

    async def post_book(self, book_data: BookSchemaPost, user_id):
        book = await self.db.book.add(book_data, author_id=user_id)
        await self.db.commit()
        return book

    async def put_book(self, book_id: int, book_data: BookSchemaRequest):
        await self.db.book.update(id=book_id, data=book_data)
        await self.db.commit()

    async def patch_book(self, book_id: int, book_data: BookSchemaPatch):
        await self.db.book.update(id=book_id, exclude_unset=True, data=book_data)
        await self.db.commit()

    async def delete_book(self, book_id: int):
        await self.db.book.delete(id=book_id)
        await self.db.commit()
