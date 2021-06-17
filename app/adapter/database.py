from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from app.config import settings

database = Database(
    settings.DATABASE_URL,
    min_size=settings.MIN_CONNECTIONS_COUNT,
    max_size=settings.MAX_CONNECTIONS_COUNT,
)

engine = create_engine(settings.DATABASE_URL)

Base = declarative_base()
