import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, Text, CheckConstraint
from src.db.base import Base

if typing.TYPE_CHECKING:
    from src.models.book import Book


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    rating: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("rating BETWEEN 1 AND 5", name="check_rating_range")
    )
    text: Mapped[str] = mapped_column(Text)

    book: Mapped["Book"] = relationship("Book", back_populates="reviews")
