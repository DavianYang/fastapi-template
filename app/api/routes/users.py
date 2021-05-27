from fastapi import APIRouter, Body, Depends, HTTPException, status

from app.api.dependencies.authentication import get_current_user
from app.config import settings
from app.models.domain.users import User
from app.models.schemas.users import UserInResponse, UserInUpdate, UserWithToken
from app.resources import strings
from app.services import jwt
from app.services.authentication import check_email_is_taken, check_username_is_taken
from app.services.users import UserService

router = APIRouter()


@router.get(
    "",
    response_model=UserInResponse,
    name="users:get-current-user",
    status_code=status.HTTP_200_OK,
)
async def retrieve_current_user(
    user: User = Depends(get_current_user),
) -> UserInResponse:
    token = jwt.create_access_token_for_user(user, str(settings.SECRET_KEY))
    return UserInResponse(
        user=UserWithToken(name=user.name, email=user.email, token=token)
    )


@router.put(
    "",
    response_model=UserInResponse,
    name="users:update-current-user",
    status_code=status.HTTP_200_OK,
)
async def update_current_user(
    current_user: User = Depends(get_current_user),
    update_user: UserInUpdate = Body(..., embed=True, alias="user"),
    user_service: UserService = Depends(UserService),
):
    if update_user.name and update_user.name != current_user.name:
        if await check_username_is_taken(user_service, update_user.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=strings.USERNAME_TAKEN
            )

    if update_user.email and update_user.email != current_user.email:
        if await check_email_is_taken(user_service, update_user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=strings.EMAIL_TAKEN
            )
    user = await user_service.update_user(user=current_user, update_user=update_user)
    token = jwt.create_access_token_for_user(user, str(settings.SECRET_KEY))
    return UserInResponse(
        user=UserWithToken(name=user.name, email=user.email, token=token)
    )
