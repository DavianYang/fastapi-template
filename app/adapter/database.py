from databases import Database
from sqlalchemy import create_engine

from app.adapter.orms.orm import metadata
from app.config import settings

database = Database(settings.DB_CONNECTION)
metadata.create_all(create_engine(settings.DB_CONNECTION))
