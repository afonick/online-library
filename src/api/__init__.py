from fastapi import APIRouter

from src.api.v1.auth import router as auth_router
from src.api.v1.users import router as users_router
from src.api.v1.books import router as books_router
from src.api.v1.reviews import router as review_router
from src.api.v1.favorites import router as favorite_router
from src.api.v1.images import router as images_router
from src.api.v1.statistics import router as statistics_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(books_router)
api_router.include_router(review_router)
api_router.include_router(favorite_router)
api_router.include_router(images_router)
api_router.include_router(statistics_router)
