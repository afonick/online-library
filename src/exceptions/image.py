from src.core.config import ALLOWED_IMAGE_EXTENSIONS
from src.exceptions.base import LibraryHTTPException


class ImageUniqueHTTPException(LibraryHTTPException):
    status_code = 409
    detail = "Файл с таким именем уже существует"


class ImageNotFoundHTTPException(LibraryHTTPException):
    status_code = 404
    detail = "Файл не найден"

class ImageErrorFormatHTTPException(LibraryHTTPException):
    status_code = 404
    detail = f"Недопустимый формат изображения. Поддерживаемые форматы: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"