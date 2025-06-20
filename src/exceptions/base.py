from fastapi import HTTPException


class LibraryException(Exception):
    detail = "Неожиданная ошибка"
    status_code = 400

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, self.status_code, *args, **kwargs)


class ObjectNotFoundException(LibraryException):
    detail = "Объект не найден"
    status_code = 404


class ObjectUniqueException(LibraryException):
    detail = "Такой объект уже существует"
    status_code = 409


class LibraryHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(self.status_code, self.detail)
