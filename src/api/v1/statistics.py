from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.utils.statistics import refresh_materialized_view
from src.dependencies.database import db_session
from src.dependencies.user import admin_dep
from src.schemas.statistics import PopularBookSchema, TopAuthorSchema, ReviewStatsSchema
from src.services.statistics import PopularBookService, TopAuthorService, ReviewStatsService

router = APIRouter(prefix="/stats", tags=["Статистика"])


@router.get(
    "/popular-books",
    response_model=list[PopularBookSchema],
    dependencies=[admin_dep],
    summary="Статистика по книгам в избранном и с отзывами (админ)"
)
@cache(expire=30)
async def get_popular_books(db: db_session):
    await refresh_materialized_view("popular_books")
    popular_books = await PopularBookService(db).get_all()
    return popular_books


@router.get(
    "/top-authors",
    response_model=list[TopAuthorSchema],
    dependencies=[admin_dep],
    summary="Статистика по авторам книг с отзывами (админ)"
)
@cache(expire=30)
async def get_top_authors(db: db_session):
    await refresh_materialized_view("top_authors")
    top_authors = await TopAuthorService(db).get_all()
    return top_authors


@router.get(
    "/review-stats",
    response_model=ReviewStatsSchema,
    dependencies=[admin_dep],
    summary="Статистика по отзывам и рейтингу (админ)"
)
@cache(expire=30)
async def get_review_stats(db: db_session):
    await refresh_materialized_view("review_stats")
    review_stats = await ReviewStatsService(db).get_one()
    return review_stats
