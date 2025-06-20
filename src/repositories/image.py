from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError

from src.db.session import engine
from src.exceptions.base import LibraryException
from src.mappers.mappers import ImageMapper
from src.models import Image, Book
from src.repositories.base import BaseRepository


class ImageRepository(BaseRepository):
    model = Image
    mapper = ImageMapper

    async def add(self, data: BaseModel, **filter_by):
        image_data = data.model_dump()
        query = select(Book).filter_by(id=image_data["book_id"])
        result = await self.session.execute(query)
        book = result.scalar_one()
        insert_stmt = insert(self.model).values(**image_data, **filter_by).returning(self.model)
        print(insert_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        try:
            result = await self.session.execute(insert_stmt)
            image = result.scalars().one()

        except IntegrityError:
            raise LibraryException

        return self.mapper.map_to_domain_entity(image)