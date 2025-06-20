from sqlalchemy import Float
from sqlalchemy.orm import Mapped, mapped_column
from src.db.base import Base


class PopularBook(Base):
    __tablename__ = "popular_books"

    book_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    review_count: Mapped[int]
    avg_rating: Mapped[float]


class BookRatingStats(Base):
    __tablename__ = "book_rating_stats"

    book_id: Mapped[int] = mapped_column(primary_key=True)
    avg_rating: Mapped[float] = mapped_column(Float, default=0)
    review_count: Mapped[int] = mapped_column(Float, default=0)


class TopAuthor(Base):
    __tablename__ = 'top_authors'

    author_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    book_count: Mapped[int]
    review_count: Mapped[int]
    avg_rating: Mapped[float]


class ReviewStats(Base):
    __tablename__ = 'review_stats'

    total_reviews: Mapped[int] = mapped_column(primary_key=True)
    avg_rating: Mapped[float]
    min_rating: Mapped[int]
    max_rating: Mapped[int]
