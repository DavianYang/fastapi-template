from databases import Database
from sqlalchemy import create_engine

from app.config import DATABASE_URL
from app.adapter.orms.orm import metadata

database = Database(DATABASE_URL)

metadata.create_all(create_engine(DATABASE_URL))

async def connect_to_db() -> None:
    await database.connect()
    
async def close_db_connect() -> None:
    await database.disconnect()