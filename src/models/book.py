import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Text
from src.db.base import Base

if typing.TYPE_CHECKING:
    from src.models.user import User
    from src.models.review import Review


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    file_path: Mapped[str] = mapped_column(String, nullable=True)  # Путь к файлу книги

    author: Mapped["User"] = relationship("User", back_populates="books")
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="book")
