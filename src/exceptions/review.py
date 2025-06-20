from src.exceptions.base import LibraryException, LibraryHTTPException


class ReviewNotFoundException(LibraryException):
    detail = "Отзыв не найден"


class NotAuthorReviewException(LibraryException):
    detail = "Вы не автор этого отзыва"


class NotUniqueReviewException(LibraryException):
    detail = "Вы уже оставляли отзыв на эту книгу, попробуйте изменить или дополнить его"


class RatingErrorException(LibraryException):
    detail = "Рейтинг должен быть в диапазоне от 1 до 5"


class ReviewNotFoundHTTPException(LibraryHTTPException):
    status_code = 404
    detail = "Отзыв не найден"


class RatingErrorHTTPException(LibraryHTTPException):
    status_code = 409
    detail = "Рейтинг должен быть в диапазоне от 1 до 5"


class NotAuthorReviewHTTPException(LibraryHTTPException):
    status_code = 409
    detail = "Вы не автор этого отзыва"


class NotUniqueReviewHTTPException(LibraryHTTPException):
    status_code = 409
    detail = "Вы уже оставляли отзыв на эту книгу, попробуйте изменить или дополнить его"
