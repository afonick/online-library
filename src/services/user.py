from src.exceptions.user import UserNotEditRoleException
from src.schemas.user import UserSchemaEditRole
from src.services.base import BaseService
from src.tasks.celery_tasks import notification_response_author


class UserService(BaseService):

    async def get_one(self, user_id: int):
        await self.db.user.get_one(id=user_id)

    async def activate_user(self, username: str, code: str):
        await self.db.user.activate(username=username, code=code, is_active=True)
        await self.db.commit()

    async def edit_user_role(self, user_id: int, user_data: UserSchemaEditRole):
        user = await self.db.user.get_one(id=user_id)
        if user.role.value == user_data.role.value:
            raise UserNotEditRoleException
        await self.db.user.update(id=user_id, exclude_unset=True, data=user_data)
        await self.db.commit()
        if user_data.role.value == "author":
            notification_response_author.delay(user_id)
        return f"Роль пользователя изменена на '{user_data.role.value}'"

    async def delete_user(self, user_id: int):
        await self.db.user.delete(id=user_id)
        await self.db.commit()
