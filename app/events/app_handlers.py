from typing import Callable

from fastapi import FastAPI

from app.events.db_handlers import close_db_connect, connect_to_db


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await connect_to_db()

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        await close_db_connect()

    return stop_app
