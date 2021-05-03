from fastapi import Depends

from app.adapter.repositories.users import UserRepository
from app.models.domain.users import UserInDB

class UserService:        
    async def create_user(
        self,
        name: str,
        email: str,
        password: str
    ):
        user_repo = UserRepository()
        user = UserInDB(name=name, email=email)
        user.hash_password(password)
        user_id = await user_repo._create(user)
        
        return {"id": user_id}