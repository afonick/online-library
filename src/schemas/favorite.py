from pydantic import BaseModel

from src.schemas.book import BookSchema


class FavoriteSchemaPost(BaseModel):
    user_id: int
    book_id: int


class FavoriteSchema(BaseModel):
    id: int
    book: BookSchema
