from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.api.utils.favorite import check_favorite_book, check_unique_favorite_book
from src.api.utils.review import check_book
from src.api.utils.statistics import refresh_materialized_view
from src.dependencies.database import db_session
from src.dependencies.pagination import Paginator, pagination_params
from src.dependencies.user import current_user_id
from src.exceptions.book import BookNotFoundHTTPException, BookNotFoundException
from src.exceptions.favorite import FavoriteNotFoundHTTPException

from src.schemas.favorite import FavoriteSchemaPost
from src.services.favorite import FavoriteService

router = APIRouter(tags=["Избранное"])


@router.get("/favorites", summary="Список книг в избранном текущего пользователя")
@cache(expire=30)
async def get_favorites(
        db: db_session,
        user_id: current_user_id,
        pagination: Paginator = Depends(pagination_params)

):
    await refresh_materialized_view("book_rating_stats")
    favorites = await FavoriteService(db).get_favorites(pagination, user_id)
    if not favorites:
        raise FavoriteNotFoundHTTPException

    return favorites


@router.post("/{book_id}/favorites", summary="Добавление книги в избранное текущего пользователем")
async def post_favorite(
        db: db_session,
        user_id: current_user_id,
        book_id: int,
):
    try:
        favorite_data = FavoriteSchemaPost(user_id=user_id, book_id=book_id)
        favorite = await FavoriteService(db).post_favorite(favorite_data)
    except BookNotFoundException:
        raise BookNotFoundHTTPException
    return {"status": "OK", "detail": f"Книга '{favorite.book.title}' добавлена в избранное!"}


@router.delete("/{book_id}/favorites", summary="Удаление книги из избранного текущего пользователем")
async def delete_favorite(db: db_session, book_id: int, user_id: current_user_id):
    await check_book(db, book_id)
    await check_favorite_book(db, book_id, user_id)
    await FavoriteService(db).delete_favorite(book_id, user_id)
    return {"status": "OK"}
