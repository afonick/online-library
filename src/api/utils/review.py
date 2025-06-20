from src.exceptions.base import ObjectNotFoundException, ObjectUniqueException
from src.exceptions.book import BookNotFoundException, BookNotFoundHTTPException
from src.exceptions.review import (
    NotAuthorReviewHTTPException, ReviewNotFoundException,
    ReviewNotFoundHTTPException, NotUniqueReviewException, RatingErrorException, NotUniqueReviewHTTPException,
    RatingErrorHTTPException
)
from src.services.review import ReviewService


async def check_author_review(db, user_id: int, review_id: int):
    try:
        await ReviewService(db).check_author(auth_user_id=user_id, review_id=review_id)
    except ObjectNotFoundException:
        raise NotAuthorReviewHTTPException


async def check_unique_review(db, user_id: int, book_id: int):
    try:
        await ReviewService(db).check_unique_review(user_id=user_id, book_id=book_id)
    except ObjectUniqueException:
        raise NotUniqueReviewException


async def check_book(db, book_id):
    try:
        await ReviewService(db).check_book(book_id)
    except BookNotFoundException:
        raise BookNotFoundHTTPException


async def check_review_book(db, review_id, book_id):
    try:
        await ReviewService(db).check_review_book(review_id, book_id)
    except ReviewNotFoundException:
        raise ReviewNotFoundHTTPException


async def check_rating(data):
    if data.rating < 1 or data.rating > 5:
        raise RatingErrorException


async def check_review_data(db, user_id, book_id, data):
    try:
        await check_book(db, book_id)
    except BookNotFoundException:
        raise BookNotFoundHTTPException
    try:
        await check_unique_review(db, user_id, book_id)
    except NotUniqueReviewException:
        raise NotUniqueReviewHTTPException
    try:
        await check_rating(data)
    except RatingErrorException:
        raise RatingErrorHTTPException
