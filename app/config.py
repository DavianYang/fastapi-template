import logging
import os
import sys
from enum import Enum
from functools import lru_cache
from typing import List, Tuple

from loguru import logger
from pydantic import BaseSettings

from app.loggings import InterceptHandler


class Environment(str, Enum):
    DEVELOPMENT = "dev"
    PRODUCTION = "prod"


class Settings(BaseSettings):
    ENV: Environment = Environment.DEVELOPMENT

    # Authorization
    HEADER_KEY: str = "Authorization"
    JWT_TOKEN_PREFIX: str = "Token"

    # Version
    MAJOR: int = 1
    MINOR: int = 0
    PATCH: str = ""
    SUFFIX: str = ""
    VERSION: str = f"{MAJOR}.{MINOR}.{PATCH}{SUFFIX}"

    # App
    PROJECT_NAME: str = "Fastapi Template"
    DEBUG: bool = False
    API_PREFIX: str = f"/api/v{MAJOR}"
    ALLOWED_HOSTS: List[str] = [""]
    PORT: int = 8000

    # Database
    DB_TYPE: str = "postgresql"
    DB_USERNAME: str = ""
    DB_HOST: str = "localhost"
    DB_PASSWORD: str = ""
    DB_PORT: int = 5431
    DB_NAME: str = ""
    DB_CONNECTION: str = (
        f"{DB_TYPE}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    MAX_CONNECTIONS_COUNT: int = 10
    MIN_CONNECTIONS_COUNT: int = 10

    # JWT
    JWT_SUBJECT: str = "access"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # one week
    SECRET_KEY: str = ""

    # Logging
    LOGGER_LEVEL: int = logging.DEBUG if ENV == "dev" else logging.INFO
    LOGGERS: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    class Config:
        env_file = os.path.join(os.pardir, ".env")
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in settings.LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=settings.LOGGER_LEVEL)]

logger.configure(handlers=[{"sink": sys.stderr, "level": settings.LOGGER_LEVEL}])
