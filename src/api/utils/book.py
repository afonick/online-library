from src.exceptions.base import ObjectUniqueException, ObjectNotFoundException
from src.exceptions.book import NotAuthorBookException, NotAuthorBookHTTPException, BookUniqueHTTPException

from src.services.book import BookService


async def check_author_book(db, user_id, book_id):
    try:
        await BookService(db).check_author(auth_user_id=user_id, book_id=book_id)
    except ObjectNotFoundException:
        raise NotAuthorBookHTTPException


async def check_unique_book(db, book_title):
    try:
        await BookService(db).check_unique(title=book_title)
    except ObjectUniqueException:
        raise BookUniqueHTTPException
