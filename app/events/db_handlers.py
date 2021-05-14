from app.adapter.database import Base, database, engine


async def connect_to_db() -> None:
    await database.connect()


async def close_db_connect() -> None:
    await database.disconnect()


def create_tables() -> None:
    Base.metadata.create_all(engine)
