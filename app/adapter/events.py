import sqlalchemy
from fastapi import FastAPI
from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker

from app.core.config import DATABASE_URL
from app.adapter.orms import orm

db = Database(DATABASE_URL)

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(DATABASE_URL))

async def connect_to_db() -> None:
    await db.connect()
    
async def close_db_connect() -> None:
    await db.disconnect()