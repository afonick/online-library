from src.repositories.favorite import FavoriteRepository
from src.repositories.image import ImageRepository
from src.repositories.statistics import PopularBookRepository, TopAuthorRepository, ReviewStatsRepository
from src.repositories.user import UserRepository
from src.repositories.book import BookRepository
from src.repositories.review import ReviewRepository


class DatabaseManager:

    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.user = UserRepository(self.session)
        self.book = BookRepository(self.session)
        self.review = ReviewRepository(self.session)
        self.favorite = FavoriteRepository(self.session)
        self.image = ImageRepository(self.session)
        self.popular_book = PopularBookRepository(self.session)
        self.top_author = TopAuthorRepository(self.session)
        self.review_stats = ReviewStatsRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
