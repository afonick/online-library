import asyncio
from celery import shared_task

from src.core.config import settings
from src.tasks.email_sender import send_email
from src.tasks.utils import (
    refresh_materialized_views, generate_excel_report,
    send_notification_creation_review, send_notification_registration_code,
    send_delayed_deleter_inactive_user, send_notification_request_author,
    send_notification_response_author
)


@shared_task
def refresh_and_report_stats():
    try:
        asyncio.run(refresh_materialized_views())
        print("Материализованные представления обновлены.")
    except Exception as e:
        print(f"Не удалось обновить материализованные представления: {e}")

    try:
        attachment_path = asyncio.run(generate_excel_report())
        send_email(
            subject="Ежедневный отчет по статистике онлайн-библиотеки.",
            body="Во вложении отчет по книгам, авторам и отзывам.",
            recipient=settings.ADMIN_EMAIL,
            attachment_path=attachment_path
        )
        print("Отчёт сгенерирован и отправлен.")
    except Exception as e:
        print(f"Не удалось сгенерировать и отправить отчёт: {e}")


@shared_task(name="send_notification_creation_review")
def notification_creation_review(review_id):
    asyncio.run(send_notification_creation_review(review_id))


@shared_task(name="send_notification_registration_code")
def notification_registration_code(user_id):
    asyncio.run(send_notification_registration_code(user_id))


@shared_task(name="send_delayed_deleter_inactive_user")
def delayed_deleter_inactive_user(user_id):
    asyncio.run(send_delayed_deleter_inactive_user(user_id))


@shared_task(name="send_notification_request_author")
def notification_request_author(user_id):
    asyncio.run(send_notification_request_author(user_id))


@shared_task(name="send_notification_response_author")
def notification_response_author(user_id):
    asyncio.run(send_notification_response_author(user_id))
