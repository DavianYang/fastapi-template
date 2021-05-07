from app.adapter.repositories.users import UserRepository
from app.errors.database import EntityDoesNotExist
from app.models.domain.users import UserInDB


class UserService:
    def __init__(self) -> None:
        self.repo = UserRepository()

    async def get_user_by_name(self, name: str):
        user_row = await self.repo._get(name)
        print(user_row)
        if user_row:
            return UserInDB(**user_row)

        raise EntityDoesNotExist(f"user with name {name} does not exist")

    async def get_user_by_email(self, email: str):
        pass

    async def create_user(self, name: str, email: str, password: str):
        user = UserInDB(name=name, email=email)
        user.hash_password(password)
        user_id = await self.repo._create(user)
        return user_id
