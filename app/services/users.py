import datetime as dt

from app.adapter.repositories.users import UserRepository
from app.errors.database import EntityDoesNotExist
from app.models.domain.users import UserInDB
from app.models.schemas.users import UserInUpdate


class UserService:
    def __init__(self) -> None:
        self.repo = UserRepository()

    async def get_user_by_id(self, id: str):
        user_row = await self.repo._get_by_id(id)
        if user_row:
            return UserInDB(**user_row)

    async def get_user_by_name(self, name: str):
        user_row = await self.repo._get_by_name(name)
        if user_row:
            return UserInDB(**user_row)

        raise EntityDoesNotExist(f"user with name {name} does not exist")

    async def get_user_by_email(self, email: str):
        user_row = await self.repo._get_by_email(email=email)
        if user_row:
            return UserInDB(**user_row)

        raise EntityDoesNotExist(f"user with email {email} does not exist")

    async def create_user(self, name: str, email: str, password: str):
        user = UserInDB(name=name, email=email)
        user.hash_password(password)
        user = await self.repo._create(user)

        return user

    async def update_user(self, user: UserInDB, update_user: UserInUpdate):
        user.name = update_user.name or user.name
        user.email = update_user.email or user.email
        user.image = update_user.image or user.image
        user.updated_at = dt.datetime.now()

        if update_user.password:
            user.hash_password(update_user.password)

        user_update = await self.repo._update(user)
        return user_update

    async def delete_user(self, user: UserInDB):
        user.is_active = False

        await self.repo._delete(user)
