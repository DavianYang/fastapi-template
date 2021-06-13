from typing import Callable

from fastapi import FastAPI
from loguru import logger

from app.config import settings
from app.events.db_handlers import close_db_connect, connect_to_db, create_tables


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        logger.opt(colors=True).info(
            f"Swagger API Documentaion: <blue><underline>http://127.0.0.1:{settings.PORT}/docs</underline></blue>"
        )
        logger.opt(colors=True).info(
            f"ReDoc API Documentaion: <blue><underline>http://127.0.0.1:{settings.PORT}/redoc</underline></blue>"
        )

        create_tables()

        await connect_to_db()

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    @logger.catch
    async def stop_app() -> None:
        await close_db_connect()

    return stop_app
