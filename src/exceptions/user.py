from src.exceptions.base import LibraryException, LibraryHTTPException


class ExistsUserException(LibraryException):
    detail = "Пользователь с таким username или email уже существует"


class IsNotActiveUserException(LibraryException):
    detail = "Пользователь не активный"


class UserNotFoundException(LibraryException):
    detail = "Пользователь не найден"


class UserActivateException(LibraryException):
    detail = "Ошибка активации пользователя"


class UserNotEditRoleException(LibraryException):
    detail = "Роль пользователя не была изменена"


class UserNotFoundHTTPException(LibraryHTTPException):
    status_code = 404
    detail = "Пользователь не найден"


class UsernameNotFoundHTTPException(LibraryHTTPException):
    status_code = 404
    detail = "Пользователя с таким именем не существует"


class UserCodeNotFoundHTTPException(LibraryHTTPException):
    status_code = 409
    detail = "Неверный код активации"


class IsNotActiveUserHTTPException(LibraryHTTPException):
    status_code = 409
    detail = "Активируйте пользователя перед входом в систему"


class UserIsActiveHTTPException(LibraryHTTPException):
    status_code = 409
    detail = "Пользователь уже был активирован"


class UserNotEditRoleHTTPException(LibraryHTTPException):
    status_code = 409
    detail = "Пользователь уже имеет выбранную роль"
