import os
from typing import List
from functools import lru_cache

from pydantic import BaseSettings, PostgresDsn

class Settings(BaseSettings):
    # Version
    MAJOR: int = 0
    MINOR: int = 0
    PATCH: str = ''
    SUFFIX: str = ''
    VERSION: str = f"{MAJOR}.{MINOR}.{PATCH}{SUFFIX}"
    
    # App
    PROJECT_NAME: str = "Fastapi Template"
    DEBUG: bool = False
    API_PREFIX: str = "/api"
    ALLOWED_HOSTS: List[str] = [""]
    
    # Database
    DB_TYPE: str = "postgresql"
    DB_USER: str = ""
    DB_HOST: str = "localhost"
    DB_PASSWORD: str = ""
    DB_PORT: int = 5431
    DB_NAME: str = ""
    DB_CONNECTION: PostgresDsn = f"{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # JWT
    JWT_SUBJECT: str = "access"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # one week
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    
@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()