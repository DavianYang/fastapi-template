from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from app.config import settings

database = Database(
    settings.DB_CONNECTION,
    min_size=settings.MIN_CONNECTIONS_COUNT,
    max_size=settings.MAX_CONNECTIONS_COUNT,
)

engine = create_engine(settings.DB_CONNECTION)

Base = declarative_base()
