from typing import Optional

from fastapi import Depends, HTTPException, Security, requests, status
from fastapi.security import APIKeyHeader
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings
from app.errors.database import EntityDoesNotExist
from app.resources import strings
from app.services import jwt
from app.services.users import UserService


class RWAPIKeyHeader(APIKeyHeader):
    async def __call__(self, request: requests.Request) -> Optional:
        try:
            return await super().__call__(request)
        except StarletteHTTPException as orginal_auth_exc:
            raise HTTPException(
                status_code=orginal_auth_exc.status_code,
                detail=strings.AUTHENTICATION_REQUIRED,
            )


def _get_authorization_header(
    api_key: str = Security(RWAPIKeyHeader(name=settings.HEADER_KEY)),
) -> str:
    try:
        token_prefix, token = api_key.split(" ")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=strings.WRONG_TOKEN_PREFIX
        )

    if token_prefix != settings.JWT_TOKEN_PREFIX:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=strings.WRONG_TOKEN_PREFIX
        )

    return token


async def get_current_user(
    token: str,
    service: UserService = Depends(UserService),
):
    try:
        username = jwt.get_username_from_token(token, str(settings.SECRET_KEY))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=strings.MALFORMED_PAYLOAD
        )

    try:
        return await service.get_user_by_name(name=username)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=strings.MALFORMED_PAYLOAD
        )


async def _get_current_user_optional(
    token, service: UserService = Depends(UserService)
):
    if token:
        return await get_current_user(service, token)
    return None
