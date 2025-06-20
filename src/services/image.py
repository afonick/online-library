import shutil

from src.api.utils.file import upload_file
from src.core.config import UPLOAD_DIR
from src.schemas.image import ImageSchemaAdd
from src.services.base import BaseService

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class ImageService(BaseService):

    @staticmethod
    async def upload_image(file, filename):
        return await upload_file(file, filename, "image")

    async def get_images(self, book_id: int):
        return await self.db.image.get_all_with_filter(book_id=book_id)

    async def get_image(self, image_id: int):
        return await self.db.image.get_one(id=image_id)

    async def get_count_with_filter(self, book_id: int):
        return await self.db.image.get_count_with_filter(book_id=book_id)

    async def add_image(self, book_id, new_name, image_url):
        image_data = ImageSchemaAdd(book_id=book_id, name=new_name, url=image_url)
        image = await self.db.image.add(image_data)
        await self.db.commit()
        return image
