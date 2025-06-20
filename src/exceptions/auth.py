from src.exceptions.base import LibraryException, LibraryHTTPException


class DecodeAccessTokenException(LibraryException):
    detail = "Неверный токен"

class DecodeAccessTokenHTTPException(LibraryHTTPException):
    status_code = 401
    detail = "Неверный токен"