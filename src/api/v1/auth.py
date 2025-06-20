from fastapi import APIRouter, Body, HTTPException, Response, Form, Path
from sqlalchemy.exc import NoResultFound

from src.api.examples.user import users_example
from src.api.utils.auth import (
    user_data_generation, check_user_data_for_activation,
    register_response, request_author
)
from src.dependencies.database import db_session
from src.dependencies.user import current_user_id, access_token_dep
from src.exceptions.user import (
    ExistsUserException, IsNotActiveUserException,
    IsNotActiveUserHTTPException
)

from src.services.auth import auth_service
from src.schemas.user import UserSchemaAdd, UserSchemaRequestAdd
from src.services.user import UserService

router = APIRouter(prefix="/auth", tags=["Регистрация и аутентификация"])


@router.post("/register", summary="Регистрация пользователя")
async def register_user(db: db_session, data: UserSchemaRequestAdd = Body(openapi_examples=users_example)):
    if not data.password:
        raise HTTPException(status_code=422, detail="Введите пароль")
    user_data = await user_data_generation(data)
    user_database = UserSchemaAdd(**user_data)
    try:
        user = await db.user.add_user(user_database)
    except ExistsUserException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()
    detail = await register_response(user)

    return {
        "status": "OK",
        "detail": detail
    }


@router.post("/activate/{username}", summary="Активация пользователя")
async def activate_user(
        db: db_session,
        username: str = Path(description="Имя пользователя"),
        code: str = Form(..., description="Код активации пользователя")
):
    await check_user_data_for_activation(db, username, code)
    await UserService(db).activate_user(username=username, code=code)

    return {"message": "Пользователь успешно активирован!"}


@router.post("/login", summary="Аутентификация пользователя")
async def login_user(db: db_session, response: Response,
                     data: UserSchemaRequestAdd = Body(openapi_examples=users_example)):
    try:
        user = await db.user.get_user_for_login(username=data.username, email=data.email)
    except NoResultFound:
        raise HTTPException(status_code=409, detail="Пользователя с таким username или email не существует")
    except IsNotActiveUserException:
        raise IsNotActiveUserHTTPException
    if not auth_service.verify_password(data.password, user.hashed_password):
        return HTTPException(status_code=409, detail="Неверный пароль")
    access_token = auth_service.create_access_token({"user_id": user.id, "user_role": user.role.value})
    response.set_cookie(key="access_token", value=access_token)

    return {"access_token": access_token}


@router.get("/me", summary="Текущий пользователь")
async def current_user(db: db_session, user_id: current_user_id):
    user = await db.user.get_one_or_none(id=user_id)

    return user


@router.get("/logout", dependencies=[access_token_dep], summary="Выход из системы")
async def logout_user(response: Response):
    response.delete_cookie("access_token")

    return {"status": "OK"}


@router.get("/author", summary="Запрос на получение роли author")
async def request_author_role(db: db_session, user_id: current_user_id):
    detail = await request_author(db, user_id)
    return {
        "status": "OK",
        "detail": detail
    }
