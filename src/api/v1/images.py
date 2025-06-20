from fastapi import APIRouter, UploadFile
from fastapi.responses import RedirectResponse

from src.api.utils.book import check_author_book
from src.api.utils.review import check_book
from src.core.config import settings
from src.dependencies.database import db_session
from src.dependencies.user import author_dep, current_user_id
from src.exceptions.base import ObjectNotFoundException
from src.exceptions.book import BookNotFoundHTTPException
from src.exceptions.image import ImageNotFoundHTTPException, ImageErrorFormatHTTPException
from src.services.book import BookService
from src.services.image import ImageService

router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post("/books/{book_id}", dependencies=[author_dep], summary="Загрузка изображения книги")
async def upload_file(db: db_session, book_id: int, user_id: current_user_id, file: UploadFile):
    await check_book(db, book_id)
    await check_author_book(db, user_id, book_id)
    count = await ImageService(db).get_count_with_filter(book_id)
    postfix = count + 1
    try:
        book = await BookService(db).get_book(book_id)
    except ObjectNotFoundException:
        raise BookNotFoundHTTPException
    image_name = f"{book.title}-{postfix}"
    try:
        new_name = await ImageService().upload_image(file, image_name)
    except ValueError:
        raise ImageErrorFormatHTTPException
    image_url = f"{settings.SITE_URL}/static/images/{new_name}"
    image = await ImageService(db).add_image(book_id, new_name, image_url)

    return {"data": image}

@router.get("/books/{book_id}", summary="Получение данных об изображениях книги")
async def get_images(db: db_session, book_id: int):
    images = await ImageService(db).get_images(book_id)
    return {"data": images}


@router.get("{image_id}", summary="Получение изображения по идентификатору")
async def get_images(db: db_session, image_id: int):
    try:
        image = await ImageService(db).get_image(image_id)
    except ObjectNotFoundException:
        raise ImageNotFoundHTTPException

    return RedirectResponse(f"{settings.SITE_URL}/static/images/{image.name}")