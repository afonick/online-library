from src.services.base import BaseService


class PopularBookService(BaseService):

    async def get_all(self):
        return await self.db.popular_book.get_all()


class TopAuthorService(BaseService):

    async def get_all(self):
        return await self.db.top_author.get_all()


class ReviewStatsService(BaseService):

    async def get_one(self):
        return await self.db.review_stats.get_one()
