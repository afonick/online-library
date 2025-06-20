from src.exceptions.base import LibraryException, LibraryHTTPException


class BookNotFoundException(LibraryException):
    detail = "Книга не найдена"


class NotAuthorBookException(LibraryException):
    detail = "Вы не автор этой книги"


class IncorrectDataBookException(LibraryException):
    detail = "Заголовок и описание книги не могут быть пустыми"


class BookNotFoundHTTPException(LibraryHTTPException):
    status_code = 404
    detail = "Книга не найдена"


class BookUniqueHTTPException(LibraryHTTPException):
    status_code = 409
    detail = "Книга с таким названием уже существует"


class NotAuthorBookHTTPException(LibraryHTTPException):
    status_code = 409
    detail = "Вы не автор этой книги"


class IncorrectDataBookHTTPException(LibraryHTTPException):
    status_code = 409
    detail = "Заголовок и описание книги не могут быть пустыми"


class ErrorBookFileHTTPException(LibraryHTTPException):
    status_code = 409
    detail = "Допускается только формат PDF"
