from loguru import logger

from app.adapter.database import Base, database, engine
from app.config import settings


async def connect_to_db() -> None:
    logger.info("Connecting  to {0}", repr(settings.DATABASE_URL))

    await database.connect()

    logger.info("Connection established")


async def close_db_connect() -> None:
    logger.info("Closing connection to database")

    await database.disconnect()

    logger.info("Connection closed")


def create_tables() -> None:
    logger.info("Creating tables")

    Base.metadata.create_all(engine)

    logger.info("Tables Created")
