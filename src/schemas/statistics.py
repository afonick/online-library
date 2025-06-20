from pydantic import BaseModel

class PopularBookSchema(BaseModel):
    book_id: int
    title: str
    review_count: int
    avg_rating: float | None

class BookRatingStatsSchema(BaseModel):
    book_id: int
    avg_rating: float | None
    review_count: int


class TopAuthorSchema(BaseModel):
    author_id: int
    username: str
    book_count: int
    review_count: int
    avg_rating: float | None

class ReviewStatsSchema(BaseModel):
    total_reviews: int
    avg_rating: float | None
    min_rating: int | None
    max_rating: int | None