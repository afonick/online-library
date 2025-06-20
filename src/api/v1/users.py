from fastapi import APIRouter, Body

from src.api.examples.user import users_roles_example
from src.api.utils.user import check_user

from src.dependencies.database import db_session
from src.dependencies.user import admin_dep
from src.exceptions.user import UserNotEditRoleException, UserNotEditRoleHTTPException
from src.schemas.user import UserSchemaEditRole
from src.services.user import UserService

router = APIRouter(prefix="/users", tags=["Управление пользователями"])


@router.get("", dependencies=[admin_dep], summary="Все пользователи (админ)")
async def get_users(db: db_session):
    users = await db.user.get_all()

    return users


@router.patch("/{user_id}", dependencies=[admin_dep], summary="Изменение пользователя (админ)")
async def edit_user_role(
        db: db_session,
        user_id: int,
        user_data: UserSchemaEditRole = Body(openapi_examples=users_roles_example)
):
    await check_user(db, user_id)
    try:
        detail = await UserService(db).edit_user_role(user_id, user_data)
    except UserNotEditRoleException:
        raise UserNotEditRoleHTTPException
    return {"status": "OK", "detail": detail}


@router.delete("/{user_id}", dependencies=[admin_dep], summary="Удаление пользователя (админ)")
async def delete_user(db: db_session, user_id: int):
    await check_user(db, user_id)
    await UserService(db).delete_user(user_id)
    return {"status": "OK"}
