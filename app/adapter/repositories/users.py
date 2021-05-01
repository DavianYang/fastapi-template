from app.adapter.repositories.base import BaseRepository
from app.adapter.orms import orm
from app.models.domain.users import User, UserInDB

class UserRepository(BaseRepository):
    async def _create(
        self,
        name: str,
        email: str,
        password: str
    ) -> UserInDB:
        user = UserInDB(name=name, email=email)
        user.hash_password(password)