import os
from enum import Enum
from functools import lru_cache
from typing import List

from pydantic import BaseSettings


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

    # JWT
    JWT_SUBJECT: str = "access"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # one week
    SECRET_KEY: str = ""

    class Config:
        env_file = os.path.join(os.pardir, ".env")
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
