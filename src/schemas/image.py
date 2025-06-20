from pydantic import BaseModel

class ImageSchemaAdd(BaseModel):
    book_id: int
    name: str
    url: str

class ImageSchema(ImageSchemaAdd):
    id: int