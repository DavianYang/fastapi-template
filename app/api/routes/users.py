from fastapi import APIRouter
from fastapi.param_functions import Depends

from app.models.domain.users import User
from app.models.schemas.users import UserInResponse, UserInUpdate, UserWithToken
from app.services.users import UserService

router = APIRouter()

# @router.get("", response_model=UserInResponse, name="users:get-current-user")
# async def get_current_user(
#     user: User,
#     service: Depends(UserService)
# ):
#     user = await service.get_user_by_name(user.name)

#     return user
