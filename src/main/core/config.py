from typing import List

from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

MAJOR = 0
MINOR = 0
PATCH = ''
SUFFIX = '' # eg.rc0

API_PREFIX = "/api"
VERSION = f"{MAJOR}.{MINOR}.{PATCH}{SUFFIX}"

config = Config('.env')

DEBUG: bool = config("DEBUG", cast=bool, default=False)

DATABASE_URL: DatabaseURL = config("DB_CONNECTION")

PROJECT_NAME: str = config("PROJECT_NAME", default="Main")
ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS",
    cast=CommaSeparatedStrings,
    default="",
)