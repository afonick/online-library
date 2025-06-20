from pydantic import BaseModel, EmailStr

from src.models import Role


class UserSchemaRequestAdd(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserSchemaAdd(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    code: str
    role: Role = Role.user
    is_active: bool = False


class UserSchemaEditRole(BaseModel):
    role: Role


class UserCodeSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    code: str


class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: Role


class UserBookSchema(BaseModel):
    id: int
    username: str


class UserSchemaLogin(UserSchema):
    role: Role
    hashed_password: str
