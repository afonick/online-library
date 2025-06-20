from typing import Annotated, List, Callable

from fastapi import Depends, Request, HTTPException
from jwt import ExpiredSignatureError

from src.services.auth import auth_service


def get_access_token(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Пользователь не аутентифицирован")
    return access_token


access_token_dep = Depends(get_access_token)


def get_current_user_data(access_token: str = access_token_dep):
    try:
        data = auth_service.decode_access_token(access_token)
        return data
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Токен истёк или недействителен")


user_data_dep = Depends(get_current_user_data)


def get_current_user_id(user_data: dict = user_data_dep):
    user_id = user_data.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user_id


current_user_id = Annotated[int, Depends(get_current_user_id)]


def require_roles(allowed_roles: List[str]) -> Callable:
    def role_dependency(user_data: dict = user_data_dep):
        user_id = user_data.get("user_id")
        user_role = user_data.get("user_role")
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Недостаточно прав! "
                       f"Ваша роль {user_role}. "
                       f"Доступно только для {' или '.join(allowed_roles)}"
            )
        return user_id

    return Depends(role_dependency)


admin_dep = require_roles(["admin"])
author_dep = require_roles(["author", "admin"])
