from src.exceptions.base import ObjectNotFoundException
from src.exceptions.user import UserNotFoundHTTPException
from src.services.user import UserService


async def check_user(db, user_id):
    try:
        await UserService(db).get_one(user_id)
    except ObjectNotFoundException:
        raise UserNotFoundHTTPException
