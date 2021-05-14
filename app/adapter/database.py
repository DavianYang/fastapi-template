from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from app.config import settings

database = Database(settings.DB_CONNECTION)

engine = create_engine(settings.DB_CONNECTION)

Base = declarative_base()
