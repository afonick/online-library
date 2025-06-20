from sqlalchemy import text
from src.db.session import async_session_maker


async def refresh_materialized_view(view_name: str):
    query = f"REFRESH MATERIALIZED VIEW {view_name};"
    async with async_session_maker() as session:
        await session.execute(text(query))
        await session.commit()
