from databases import Database
import databases
from fastapi import Depends
from sqlalchemy import create_engine

from app.config import get_settings, Settings
from app.adapter.orms.orm import metadata

database = Database(get_settings().DB_CONNECTION)
metadata.create_all(create_engine(get_settings().DB_CONNECTION))
    
async def connect_to_db() -> None:
    await database.connect()

async def close_db_connect() -> None:
    await database.disconnect()