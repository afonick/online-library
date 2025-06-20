from src.exceptions.base import ObjectNotFoundException, LibraryException, ObjectUniqueException, LibraryHTTPException
from src.exceptions.book import BookNotFoundException
from src.exceptions.review import ReviewNotFoundException, RatingErrorException
from src.schemas.review import ReviewSchemaPostPut, ReviewSchemaPatch, ReviewSchemaRequest
from src.services.base import BaseService


class ReviewService(BaseService):

    async def check_author(self, auth_user_id: int, review_id: int):
        await self.db.review.check_author(auth_user_id, user_id=auth_user_id, id=review_id)

    async def check_book(self, book_id: int):
        await self.db.review.check_book(book_id)

    async def check_review_book(self, review_id: int, book_id: int):
        await self.db.review.check_review_book(review_id, book_id)

    async def get_all(self, pagination):
        page = pagination.page
        per_page = pagination.per_page
        return await self.db.review.get_all(limit=per_page, offset=(page - 1) * per_page)

    async def get_book_reviews(self, book_id):
        return await self.db.review.get_book_reviews(book_id)

    async def get_review(self, review_id: int):
        try:
            review = await self.db.review.get_one(id=review_id)
        except ObjectNotFoundException:
            raise ReviewNotFoundException
        return review

    async def check_unique_review(self, user_id: int, book_id: int):
        if await self.db.review.get_one_or_none(user_id=user_id, book_id=book_id):
            raise ObjectUniqueException

    async def post_review(self, review_data: ReviewSchemaPostPut, user_id: int):

        review = await self.db.review.add(review_data, user_id=user_id)
        await self.db.commit()

        return review

    async def put_review(self, review_id: int, book_id: int, review_data: ReviewSchemaRequest):
        _review_data = ReviewSchemaPostPut(book_id=book_id, **review_data.model_dump())
        await self.db.review.update(id=review_id, data=_review_data)
        await self.db.commit()

    async def patch_review(self, review_id: int, book_id: int, review_data: ReviewSchemaPatch):
        await self.db.review.update(id=review_id, book_id=book_id, data=review_data, exclude_unset=True)
        await self.db.commit()

    async def delete_review(self, review_id: int, book_id: int):
        await self.db.review.delete(id=review_id, book_id=book_id)
        await self.db.commit()
