from databases import Database
from sqlalchemy import create_engine

from app.config import settings
from app.adapter.orms.orm import metadata

database = Database(settings.DB_CONNECTION)
metadata.create_all(create_engine(settings.DB_CONNECTION))