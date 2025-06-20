from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey

from src.db.base import Base


class Image(Base):
    __tablename__ = 'images'
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))
    name: Mapped[str] = mapped_column(String(100))
    url: Mapped[str] = mapped_column(String(100))