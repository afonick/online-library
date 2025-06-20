from typing import Optional

from fastapi import APIRouter, UploadFile, File, Depends, Query
from fastapi_cache.decorator import cache

from src.api.utils.book import check_author_book, check_unique_book
from src.api.utils.statistics import refresh_materialized_view
from src.core.config import settings
from src.dependencies.database import db_session
from src.dependencies.pagination import Paginator, pagination_params
from src.dependencies.user import author_dep, current_user_id
from src.exceptions.base import ObjectNotFoundException
from src.exceptions.book import BookNotFoundHTTPException, ErrorBookFileHTTPException
from src.schemas.book import BookSchemaPost, BookSchemaPatch, BookSchemaRequest
from src.services.book import BookService

router = APIRouter(prefix="/books", tags=["Книги"])


@router.get("", summary="Все книги")
@cache(expire=30)
async def get_books(
        db: db_session,
        pagination: Paginator = Depends(pagination_params),
        avg_rating: Optional[float] = Query(None, ge=0, le=5, description="Средний рейтинг книги больше или равен"),
        review_count: Optional[int] = Query(None, ge=0, description="Количество отзывов больше или равно"),
        title: Optional[str] = Query(None, description="Заголовок содержит"),
        description: Optional[str] = Query(None, description="Описание содержит"),
):
    await refresh_materialized_view("book_rating_stats")
    book = await BookService(db).get_all(pagination, avg_rating, review_count, title, description)
    return book


@router.get("/{book_id}", summary="Книга по идентификатору")
@cache(expire=30)
async def get_book(db: db_session, book_id: int, ):
    try:
        return await BookService(db).get_book(book_id)
    except ObjectNotFoundException:
        raise BookNotFoundHTTPException


@router.post("", dependencies=[author_dep], summary="Добавление книги")
async def post_book(
        db: db_session,
        user_id: current_user_id,
        book_data_request: BookSchemaRequest = Depends(BookSchemaRequest.as_form),
        document: UploadFile = File(...),
):
    await check_unique_book(db, book_data_request.title)
    try:
        doc_name = await BookService().upload_document(document, book_data_request.title)
    except ValueError:
        raise ErrorBookFileHTTPException
    file_path = f"{settings.SITE_URL}/static/documents/{doc_name}"
    book_data = BookSchemaPost(**book_data_request.model_dump(), file_path=file_path)
    book = await BookService(db).post_book(book_data, user_id)

    return {"status": "OK", "data": book}


@router.put("/{book_id}", dependencies=[author_dep], summary="Полное изменение книги")
async def put_book(db: db_session, book_id: int, user_id: current_user_id, book_data: BookSchemaRequest):
    await check_author_book(db, user_id, book_id)
    await BookService(db).put_book(book_id, book_data)
    return {"status": "OK"}


@router.patch("/{book_id}", dependencies=[author_dep], summary="Частичное изменение книги")
async def patch_book(db: db_session, book_id: int, user_id: current_user_id, book_data: BookSchemaPatch):
    await check_author_book(db, user_id, book_id)
    await BookService(db).patch_book(book_id, book_data)
    return {"status": "OK"}


@router.delete("/{book_id}", dependencies=[author_dep], summary="Удаление книги")
async def delete_book(db: db_session, book_id: int, user_id: current_user_id):
    await check_author_book(db, user_id, book_id)
    await BookService(db).delete_book(book_id)
    return {"status": "OK"}
