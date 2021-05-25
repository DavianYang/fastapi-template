from databases import Database
from pydantic import EmailStr
from sqlalchemy import Table
from sqlalchemy.sql.selectable import Select

from app.adapter.database import database
from app.adapter.orms.user import users
from app.adapter.repositories.base import BaseRepository
from app.models.domain.users import UserInDB


class UserRepository(BaseRepository):
    def __init__(self, users: Table = users, database: Database = database) -> None:
        self.database = database
        self.users = users

    async def _get(self, query: Select):
        return await self.database.fetch_one(query)

    async def _get_by_email(self, email: EmailStr):
        get_query = self.users.select().where(self.users.c.email == email)
        return await self._get(get_query)

    async def _get_by_name(self, name: str):
        get_query = self.users.select().where(self.users.c.name == name)
        return await self._get(get_query)

    async def _create(self, user: UserInDB):
        user_dict = user.dict()
        create_query = self.users.insert()
        await self.database.execute(create_query, user_dict)
        return user

    async def _update(self, user: UserInDB):
        user_dict = user.dict()
        update_query = (
            self.users.update().where(self.users.c.id == user.id).values(user_dict)
        )
        await self.database.execute(update_query)
        return user

    async def _delete(self):
        return await super()._delete()
