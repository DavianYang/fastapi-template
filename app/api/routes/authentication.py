from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.config import settings
from app.models.schemas.users import UserInCreate, UserInLogin, UserInResponse
from app.resources import strings
from app.services import jwt
from app.services.authentication import (check_email_is_taken,
                                         check_username_is_taken)
from app.services.users import UserService

router = APIRouter()


@router.post("/login", response_model=UserInResponse, name="auth:login")
async def login(
    user_login: UserInLogin,
):
    raise NotImplementedError


@router.post(
    "",
    status_code=HTTP_201_CREATED,
    # response_model=UserInResponse,
    name="auth:register",
)
async def register(
    user_create: UserInCreate = Body(..., embed=True, alias="user"),
    user_service: UserService = Depends(UserService),
):
    if await check_username_is_taken(user_service, user_create.name):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=strings.USERNAME_TAKEN
        )

    if await check_email_is_taken(user_service, user_create.email):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=strings.EMAIL_TAKEN
        )

    user = await user_service.create_user(**user_create.dict())

    token = jwt.create_access_token_for_user(user, str(settings.SECRET_KEY))

    return token
