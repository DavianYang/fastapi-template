from fastapi import APIRouter, Depends

from app.api.dependencies.authentication import get_current_user_authorizer
from app.config import settings
from app.models.domain.users import User
from app.models.schemas.users import UserInResponse, UserWithToken
from app.services import jwt

router = APIRouter()


@router.get("", response_model=UserInResponse, name="users:get-current-user")
async def retrieve_current_user(
    user: User = Depends(get_current_user_authorizer()),
) -> UserInResponse:
    token = jwt.create_access_token_for_user(user, str(settings.SECRET_KEY))
    return UserInResponse(
        user=UserWithToken(name=user.name, email=user.email, token=token)
    )
