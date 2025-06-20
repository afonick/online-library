import os
import pandas as pd
from datetime import datetime, timezone
from pathlib import Path
from sqlalchemy import text

from src.core.config import settings
from src.db.manager import DatabaseManager
from src.db.session import async_session_maker_null_pool
from src.db.session import async_session_maker
from src.tasks.email_sender import send_email


async def send_notification_registration_code(user_id):
    async with DatabaseManager(session_factory=async_session_maker_null_pool) as db:
        user = await db.user.get_user(id=user_id)
        subject = "Код активации"
        username = user.username
        user_email = user.email
        user_code = user.code
        body = (f"Здравствуйте, {username}! " +
                "Вы зарегистрировались на нашем ресурсе 'Онлайн-библиотека'!\n" +
                "Для входа в систему необходимо активировать аккаунт! " +
                "Период активации 72 часа! После чего неактивный пользователь будет удалён! " +
                f"Код активации аккаунта: {user_code}")
        send_email(subject, body, user_email)


async def send_notification_request_author(user_id):
    async with DatabaseManager(session_factory=async_session_maker_null_pool) as db:
        user = await db.user.get_user(id=user_id)
        subject = "Запрос на изменение роли"
        email = settings.ADMIN_EMAIL
        body = (f"Пользователь с идентификатором '{user.id}' и именем '{user.username}' " +
                "запросил изменение роли на 'author'!")
        send_email(subject, body, email)


async def send_notification_response_author(user_id):
    async with DatabaseManager(session_factory=async_session_maker_null_pool) as db:
        user = await db.user.get_user(id=user_id)
        subject = "Изменение роли"
        email = user.email
        body = (f"Здравствуйте, {user.username}! " +
                "Роль аккаунта была изменена на 'author'!")
        send_email(subject, body, email)


async def send_delayed_deleter_inactive_user(user_id):
    async with DatabaseManager(session_factory=async_session_maker_null_pool) as db:
        user = await db.user.get_user(id=user_id)
        if not user.is_active:
            print("Удаление неактивного пользователя!")
            await db.user.delete(id=user_id)
            await db.commit()


async def send_notification_creation_review(review_id):
    async with DatabaseManager(session_factory=async_session_maker_null_pool) as db:
        review = await db.review.get_one(id=review_id)
        book = await db.book.get_one(id=review.book_id)
        book_author = await db.user.get_one(id=book.author_id)
        review_user = await db.user.get_one(id=review.user_id)
        subject = "Уведомление о создании отзыва"
        username = book_author.username
        user_email = book_author.email
        body = f"Здравствуйте, {username}!" + \
               f" На вашу книгу '{book.title}' был оставлен отзыв '{review.text}'" + \
               f" пользователем {review_user.username} и выставлен рейтинг {review.rating}!"
        send_email(subject, body, user_email)


async def refresh_materialized_views():
    queries = [
        "REFRESH MATERIALIZED VIEW popular_books;",
        "REFRESH MATERIALIZED VIEW book_rating_stats;",
        "REFRESH MATERIALIZED VIEW top_authors;",
        "REFRESH MATERIALIZED VIEW review_stats;",
    ]
    async with async_session_maker() as session:
        for query in queries:
            await session.execute(text(query))
        await session.commit()


def pydantic_to_dataframe(models) -> pd.DataFrame:
    if isinstance(models, list):
        return pd.DataFrame([m.model_dump() for m in models])
    else:
        return pd.DataFrame([models.model_dump()])


async def generate_excel_report():
    async with DatabaseManager(session_factory=async_session_maker_null_pool) as db:
        # Получаем данные
        popular_books = await db.popular_book.get_all()
        top_authors = await db.top_author.get_all()
        review_stats = await db.review_stats.get_one()

        # Получаем DataFrame
        df_books = pydantic_to_dataframe(popular_books)
        df_authors = pydantic_to_dataframe(top_authors)
        df_reviews = pydantic_to_dataframe(review_stats)

        # Сохраняем в Excel
        filename = f"report_{datetime.now(timezone.utc).strftime('%Y-%m-%d_%Hh%Mm%Ss')}.xlsx"
        path = os.path.join("src", "static", "reports", filename)
        posix_path = Path(path).as_posix()
        os.makedirs("src/static/reports", exist_ok=True)

        with pd.ExcelWriter(path) as writer:
            df_books.to_excel(writer, sheet_name="Popular Books", index=False)
            df_authors.to_excel(writer, sheet_name="Top Authors", index=False)
            df_reviews.to_excel(writer, sheet_name="Review Stats", index=False)

        return posix_path
