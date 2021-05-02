from app.events.db_handlers import database
from app.adapter.repositories.base import BaseRepository
from app.adapter.orms.orm import users
from app.models.domain.users import User, UserInDB

class UserRepository(BaseRepository):
    async def _get(self):
        return await super()._get()
    
    async def _create(
        self,
        name: str,
        email: str,
        password: str
    ):
        user = UserInDB(name=name, email=email)
        user.hash_password(password)
        
        query = users.insert().values(name=name, email=email, password=password)
        user_id = await database.execute(query)
        
        return {**user.dict(), "id": user_id}
    
    async def _update(self):
        return await super()._update()
    
    async def _delete(self):
        return await super()._delete()