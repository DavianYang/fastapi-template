from fastapi import APIRouter, Body, Depends, HTTPException, status

from app.config import settings
from app.errors.database import EntityDoesNotExist
from app.models.schemas.users import (
    UserInCreate,
    UserInLogin,
    UserInResponse,
    UserWithToken,
)
from app.resources import strings
from app.services import jwt
from app.services.authentication import check_email_is_taken, check_username_is_taken
from app.services.users import UserService

router = APIRouter()


@router.post(
    "/login",
    response_model=UserInResponse,
    name="auth:login",
    status_code=status.HTTP_200_OK,
)
async def login(
    user_login: UserInLogin = Body(..., embed=True, alias="user"),
    user_service: UserService = Depends(UserService),
):
    wrong_login_error = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail=strings.INCORRECT_LOGIN_INPUT
    )

    try:
        user = await user_service.get_user_by_email(email=user_login.email)
    except EntityDoesNotExist as exc_error:
        raise wrong_login_error from exc_error

    if not user.check_password(user_login.password):
        raise wrong_login_error

    token = jwt.create_access_token_for_user(user, str(settings.SECRET_KEY))

    return UserInResponse(
        user=UserWithToken(name=user.name, email=user.email, token=token)
    )


@router.post(
    "",
    response_model=UserInResponse,
    name="auth:register",
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_create: UserInCreate = Body(..., embed=True, alias="user"),
    user_service: UserService = Depends(UserService),
):
    if await check_username_is_taken(user_service, user_create.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.USERNAME_TAKEN
        )

    if await check_email_is_taken(user_service, user_create.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.EMAIL_TAKEN
        )

    user = await user_service.create_user(**user_create.dict())

    token = jwt.create_access_token_for_user(user, str(settings.SECRET_KEY))

    return UserInResponse(
        user=UserWithToken(name=user.name, email=user.email, token=token)
    )
