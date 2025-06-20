from fastapi import Query
from pydantic import BaseModel


class Paginator(BaseModel):
    page: int = 1
    per_page: int = 5

def pagination_params(
    page: int = Query(1, ge=1, description="Номер страницы"),
    per_page: int = Query(5, ge=1, le=20, description="Количество записей на странице")
) -> Paginator:
    return Paginator(page=page, per_page=per_page)


