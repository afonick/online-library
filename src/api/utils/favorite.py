from src.exceptions.book import BookNotFoundException, BookNotFoundHTTPException
from src.exceptions.favorite import (
    FavoriteBookNotFoundException, FavoriteBookNotUniqueException,
    FavoriteBookNotFoundHTTPException, FavoriteBookNotUniqueHTTPException
)
from src.services.favorite import FavoriteService


async def check_book(db, book_id):
    try:
        await FavoriteService(db).check_book(book_id)
    except BookNotFoundException:
        raise BookNotFoundHTTPException


async def check_favorite_book(db, book_id, user_id):
    try:
        await FavoriteService(db).check_favorite_book(book_id, user_id)
    except FavoriteBookNotFoundException:
        raise FavoriteBookNotFoundHTTPException


async def check_unique_favorite_book(db, book_id, user_id):
    try:
        await FavoriteService(db).check_unique_favorite_book(book_id, user_id)
    except FavoriteBookNotUniqueException:
        raise FavoriteBookNotUniqueHTTPException
