from databases import Database

from app.adapter.orms.orm import users
from app.adapter.repositories.base import BaseRepository
from app.events.db_handlers import database
from app.models.domain.users import UserInDB


class UserRepository(BaseRepository):
    def __init__(self, database: Database = database) -> None:
        self.database = database

    async def _get(self, entity: str):
        return await self.database.fetch_one(users.select(entity))

    async def _create(self, user: UserInDB):
        return await self.database.execute(
            users.insert().values(
                name=user.name, email=user.email, password=user.hashed_password
            )
        )

    async def _update(self):
        return await super()._update()

    async def _delete(self):
        return await super()._delete()
