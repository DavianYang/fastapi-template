from fastapi import APIRouter

from app.models.domain.users import User
from app.models.schemas.users import UserInResponse, UserInUpdate, UserWithToken
from app.adapter.repositories.users import UserRepository

router = APIRouter()

@router.get("", response_model=UserInResponse, name="users:get-current-user")
async def get_current_user(
    user: User
):
    raise NotImplementedError