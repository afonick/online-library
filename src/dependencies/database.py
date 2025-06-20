from typing import Annotated

from fastapi import Depends

from src.db.manager import DatabaseManager
from src.db.session import async_session_maker


async def get_db():
    async with DatabaseManager(session_factory=async_session_maker) as db:
        yield db


db_session = Annotated[DatabaseManager, Depends(get_db)]