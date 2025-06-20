from fastapi import Form
from pydantic import BaseModel, ConfigDict, field_validator, ValidationError

from src.exceptions.book import IncorrectDataBookException
from src.schemas.user import UserBookSchema


class BookSchemaRequest(BaseModel):
    title: str
    description: str

    @classmethod
    def as_form(
            cls,
            title: str = Form(...),
            description: str = Form(...),
    ):
        try:
            return cls(title=title, description=description)
        except ValidationError:
            raise IncorrectDataBookException

    @field_validator("title", "description")
    def not_empty(cls, value):
        if not value.strip():
            raise ValueError("Поле не может быть пустым")
        return value

    model_config = ConfigDict(extra="forbid")


class BookSchemaPost(BookSchemaRequest):
    file_path: str | None = None


class BookSchema(BaseModel):
    id: int
    author_id: int
    title: str
    description: str
    file_path: str | None = None
    avg_rating: float | None = 0.0
    review_count: int | None = 0

    class Config:
        from_attributes = True


class BookAuthorSchema(BaseModel):
    id: int
    author: UserBookSchema
    title: str
    description: str
    file_path: str | None = None


class BookSchemaPatch(BookSchemaRequest):
    title: str | None = None
    description: str | None = None
