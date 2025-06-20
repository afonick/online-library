from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from src.api.utils.review import check_author_review, check_book, check_review_book, check_unique_review, check_rating, \
    check_review_data
from src.dependencies.database import db_session
from src.dependencies.pagination import Paginator, pagination_params
from src.dependencies.user import admin_dep, current_user_id
from src.exceptions.base import LibraryException, LibraryHTTPException
from src.exceptions.book import BookNotFoundHTTPException, BookNotFoundException
from src.exceptions.review import (
    RatingErrorException, RatingErrorHTTPException, ReviewNotFoundException,
    ReviewNotFoundHTTPException, NotUniqueReviewException, NotUniqueReviewHTTPException
)
from src.schemas.review import ReviewSchemaRequest, ReviewSchemaPostPut, ReviewSchemaPatch
from src.tasks.celery_tasks import notification_creation_review
from src.services.review import ReviewService

router = APIRouter(tags=["Отзывы"])


@router.get("/reviews", dependencies=[admin_dep], summary="Все отзывы (админ)")
@cache(expire=30)
async def get_reviews(db: db_session, pagination: Paginator = Depends(pagination_params)):
    review = await ReviewService(db).get_all(pagination)
    return review


@router.get("/reviews/{review_id}", summary="Получение отзыва по идентификатору")
@cache(expire=30)
async def get_review(db: db_session, review_id: int, ):
    try:
        return await ReviewService(db).get_review(review_id)
    except ReviewNotFoundException:
        raise ReviewNotFoundHTTPException


@router.get("/{book_id}/reviews", summary="Получение всех отзывов на книгу")
@cache(expire=30)
async def get_book_reviews(db: db_session, book_id: int, ):
    try:
        return await ReviewService(db).get_book_reviews(book_id)
    except BookNotFoundException:
        raise BookNotFoundHTTPException


@router.post("/{book_id}/reviews", summary="Добавление отзыва на книгу")
async def post_review(
        db: db_session,
        user_id: current_user_id,
        book_id: int,
        review_data_request: ReviewSchemaRequest,
):
    await check_review_data(db, user_id, book_id, review_data_request)
    try:
        review_data = ReviewSchemaPostPut(book_id=book_id, **review_data_request.model_dump())
        review = await ReviewService(db).post_review(review_data, user_id)
        notification_creation_review.delay(review.id)
    except LibraryException:
        raise LibraryHTTPException

    return {"status": "OK", "data": review}


@router.put("/{book_id}/reviews/{review_id}", summary="Полное изменение отзыва на книгу")
async def put_review(db: db_session, book_id: int, review_id: int, user_id: current_user_id,
                     review_data: ReviewSchemaRequest):
    await check_book(db, book_id)
    await check_review_book(db, book_id, review_id)
    await check_author_review(db, user_id, review_id=review_id)
    try:
        await ReviewService(db).put_review(book_id, review_id, review_data)
    except RatingErrorException:
        raise RatingErrorHTTPException
    return {"status": "OK"}


@router.patch("/{book_id}/reviews/{review_id}", summary="Частичное изменение отзыва на книгу")
async def patch_review(db: db_session, book_id: int, review_id: int, user_id: current_user_id,
                       review_data: ReviewSchemaPatch):
    await check_book(db, book_id)
    await check_review_book(db, book_id, review_id)
    await check_author_review(db, user_id, review_id=review_id)
    try:
        await ReviewService(db).patch_review(book_id, review_id, review_data)
    except RatingErrorException:
        raise RatingErrorHTTPException
    return {"status": "OK"}


@router.delete("/{book_id}/reviews/{review_id}", summary="Удаление отзыва на книгу")
async def delete_review(db: db_session, book_id: int, review_id: int, user_id: current_user_id):
    await check_book(db, book_id)
    await check_review_book(db, book_id, review_id)
    await check_author_review(db, user_id, review_id=review_id)
    await ReviewService(db).delete_review(book_id, review_id)
    return {"status": "OK"}
