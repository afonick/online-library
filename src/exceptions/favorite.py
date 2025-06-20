from src.exceptions.base import LibraryException, LibraryHTTPException


class FavoriteNotFoundException(LibraryException):
    detail = "У вас в избранном нет ни одной книги"


class FavoriteNotFoundHTTPException(LibraryHTTPException):
    status_code = 404
    detail = "У вас в избранном нет ни одной книги"


class FavoriteBookNotFoundException(LibraryException):
    detail = "Эта книга отсутствует в вашем избранном"


class FavoriteBookNotUniqueException(LibraryException):
    detail = "Эта книга уже в вашем избранном"


class FavoriteBookNotFoundHTTPException(LibraryHTTPException):
    status_code = 404
    detail = "Эта книга отсутствует в вашем избранном"


class FavoriteBookNotUniqueHTTPException(LibraryHTTPException):
    status_code = 404
    detail = "Эта книга уже в вашем избранном"
