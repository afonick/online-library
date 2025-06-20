import random
from string import hexdigits
from datetime import datetime, timezone, timedelta

from src.core.config import settings
from src.exceptions.user import (
    UserNotFoundException, UsernameNotFoundHTTPException,
    UserIsActiveHTTPException, UserCodeNotFoundHTTPException
)
from src.services.auth import auth_service
from src.tasks.celery_tasks import notification_registration_code, delayed_deleter_inactive_user, \
    notification_request_author


async def user_data_generation(data) -> dict:
    hashed_password = auth_service.hashed_password(data.password)
    code = "".join(random.sample(hexdigits, 7))
    user_data = {
        "username": data.username,
        "email": data.email,
        "code": code,
        "hashed_password": hashed_password
    }
    admin_name = settings.ADMIN_NAME
    admin_email = settings.ADMIN_EMAIL
    admin_password = settings.ADMIN_PASSWORD
    if all(
            [
                data.username == admin_name,
                data.email == admin_email,
                data.password == admin_password
            ]
    ):
        user_data["role"] = "admin"
        user_data["is_active"] = True
        user_data["code"] = "applied"
    return user_data


async def register_response(user) -> str:
    if user.role.value == "admin":
        detail = "Успешная регистрация администратора!"
    else:
        notification_registration_code.delay(user.id)
        eta = datetime.now(timezone.utc) + timedelta(hours=72)
        delayed_deleter_inactive_user.apply_async(args=[user.id], eta=eta)
        detail = f"Успешная регистрация! На почту {user.email} отправлено письмо с кодом активации!"

    return detail


async def check_user_data_for_activation(db, username, code) -> None:
    try:
        await db.user.get_one(username=username)
    except UserNotFoundException:
        raise UsernameNotFoundHTTPException
    try:
        await db.user.get_one(username=username, is_active=False)
    except UserNotFoundException:
        raise UserIsActiveHTTPException
    try:
        await db.user.get_one(username=username, code=code)
    except UserNotFoundException:
        raise UserCodeNotFoundHTTPException


async def request_author(db, user_id):
    user = await db.user.get_one(id=user_id)
    if user.role.value == "admin":
        detail = "Пользователь уже автор!"
    else:
        notification_request_author.delay(user_id)
        detail = "Запрос успешно создан! Ответ вам будет направлен на почту, указанную при регистрации!"
    return detail
