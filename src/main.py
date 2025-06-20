import sys
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

sys.path.append(str(Path(__file__).parent.parent))

from src.api import api_router
from src.core.redis import redis_connector
from src.api.examples.api_description import description
from src.exceptions.base import LibraryException


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_connector.connect()
    FastAPICache.init(RedisBackend(redis_connector.redis), prefix="fastapi-cache")
    yield
    await redis_connector.disconnect()


app = FastAPI(
    lifespan=lifespan,
    title="Rest API для сайта онлайн-библиотеки",
    version="1.0.0",
    description=description
)

app.include_router(api_router)


@app.exception_handler(LibraryException)
async def app_exception_handler(request: Request, exc: LibraryException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.get("/", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


app.mount("/static", StaticFiles(directory="src/static"), name="static")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"])

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', reload=True)
