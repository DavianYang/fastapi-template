from app.adapter.database import database


async def connect_to_db() -> None:
    await database.connect()


async def close_db_connect() -> None:
    await database.disconnect()
