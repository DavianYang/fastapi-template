import pytest

from app.adapter.repositories.base import BaseRepository
from app.models.domain.users import UserInDB
from app.services.users import UserService


class FakeUserRepository(BaseRepository):
    def __init__(self, users) -> None:
        self._users = set(users)

    async def _get(self, id: str):
        return next(user for user in self._users if user.id == id)

    async def _create(self, user: UserInDB):
        self._users.add(user)

    async def _update(self):
        return await super()._update()

    async def _delete(self):
        return await super()._delete()


service = UserService()


@pytest.mark.asyncio
async def test_register_user():
    repo = FakeUserRepository([])
    user_id = await service.create_user("johndoe", "johndoe@gmail.com", "123456789")
    assert repo._get(user_id) is not None
