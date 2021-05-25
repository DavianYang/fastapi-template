from fastapi import APIRouter, Body, Depends, HTTPException
from starlette import status

from app.api.dependencies.authentication import _get_current_user
from app.config import settings
from app.models.domain.users import User
from app.models.schemas.users import UserInResponse, UserInUpdate, UserWithToken
from app.resources import strings
from app.services import jwt
from app.services.authentication import check_email_is_taken, check_username_is_taken
from app.services.users import UserService

router = APIRouter()


@router.get("", response_model=UserInResponse, name="users:get-current-user")
async def retrieve_current_user(
    user: User = Depends(_get_current_user),
) -> UserInResponse:
    token = jwt.create_access_token_for_user(user, str(settings.SECRET_KEY))
    return UserInResponse(
        user=UserWithToken(name=user.name, email=user.email, token=token)
    )


@router.put("", response_model=UserInResponse, name="users:update-current-user")
async def update_current_user(
    user_update: UserInUpdate = Body(..., embed=True, alias="user"),
    current_user: User = Depends(_get_current_user),
    user_service: UserService = Depends(UserService),
):
    if user_update.name and user_update.name != current_user.name:
        if await check_username_is_taken(user_service, user_update.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=strings.USERNAME_TAKEN
            )

    if user_update.email and user_update.email != current_user.email:
        if await check_email_is_taken(user_service, user_update.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=strings.EMAIL_TAKEN
            )

    # user = await user_service.update_us
