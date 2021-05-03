import os
from typing import List
from functools import lru_cache

from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Main"
    DEBUG: bool = False
    API_PREFIX: str = "/api"
    
    MAJOR: int = 0
    MINOR: int = 0
    PATCH: str = ''
    SUFFIX: str = ''
    
    VERSION: str = f"{MAJOR}.{MINOR}.{PATCH}{SUFFIX}"
    
    ALLOWED_HOSTS: List[str] = [""]
    DB_CONNECTION: str = None
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    
@lru_cache()
def get_settings():
    return Settings()