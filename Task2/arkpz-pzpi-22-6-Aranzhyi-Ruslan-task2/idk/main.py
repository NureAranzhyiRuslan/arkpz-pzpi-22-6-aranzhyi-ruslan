from contextlib import asynccontextmanager
from pathlib import Path

from aerich import Command
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from tortoise import Tortoise
from tortoise.contrib.fastapi import RegisterTortoise

from . import config
from .routers import auth, user, sensors, measurements, forecast
from .utils.custom_exception import CustomMessageException


@asynccontextmanager
async def migrate_and_connect_orm(app_: FastAPI):  # pragma: no cover
    if not config.IS_DEBUG:
        migrations_dir = "data/migrations"

        command = Command({
            "connections": {"default": config.DB_CONNECTION_STRING},
            "apps": {"models": {"models": ["idk.models", "aerich.models"], "default_connection": "default"}},
        }, location=migrations_dir)
        await command.init()
        if Path(migrations_dir).exists():
            await command.migrate()
            await command.upgrade(True)
        else:
            await command.init_db(True)
        await Tortoise.close_connections()

    async with RegisterTortoise(
            app=app_,
            db_url=config.DB_CONNECTION_STRING,
            modules={"models": ["idk.models"]},
            generate_schemas=True,
    ):
        yield


app = FastAPI(
    lifespan=migrate_and_connect_orm,
    debug=config.IS_DEBUG,
    openapi_url="/openapi.json" if config.IS_DEBUG else None,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=(["*"] if config.IS_DEBUG else [])
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(sensors.router)
app.include_router(measurements.router)
app.include_router(forecast.router)


@app.exception_handler(CustomMessageException)
async def custom_message_exception_handler(_, exc: CustomMessageException) -> JSONResponse:
    return JSONResponse({
        "errors": exc.messages,
    }, status_code=exc.status_code)
