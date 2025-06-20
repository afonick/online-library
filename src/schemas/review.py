from pydantic import BaseModel, ConfigDict, field_validator


class ReviewSchemaRequest(BaseModel):
    text: str
    rating: int

    model_config = ConfigDict(extra="forbid")

    @field_validator("text")
    def not_empty(cls, value):
        if not value.strip():
            raise ValueError("Поле не может быть пустым")
        return value


class ReviewSchemaPostPut(BaseModel):
    book_id: int
    text: str
    rating: int


class ReviewSchema(BaseModel):
    id: int
    user_id: int
    book_id: int
    text: str
    rating: int


class ReviewSchemaPatch(BaseModel):
    text: str | None = None
    rating: int | None = None

    model_config = ConfigDict(extra="forbid")
