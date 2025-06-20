from typing import Literal
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "static"

ALLOWED_IMAGE_EXTENSIONS = ['.png', '.jpeg', '.jpg', '.gif', '.bmp', '.webp']


class Settings(BaseSettings):
    MODE: Literal["TEST", "LOCAL", "DEV", "PROD"]
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = Field(..., repr=False)
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    REDIS_HOST: str
    REDIS_PORT: int
    EMAIL_BACKEND: str
    SMTP_SERVER: str
    SMTP_PORT_SSL: int
    SMTP_PORT_TLS: int
    EMAIL_HOST_USER: str
    SENDER_PASSWORD: str = Field(..., repr=False)
    SENDER_EMAIL: str
    USE_SSL: bool
    SITE_URL: str
    ADMIN_EMAIL: str
    ADMIN_NAME: str
    ADMIN_PASSWORD: str

    SECRET_KEY: str = Field(..., repr=False)
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    @computed_field
    def REDIS_URL(self) -> str:
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}'

    @computed_field
    def DB_URL(self) -> str:
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = 'allow'


settings = Settings()
