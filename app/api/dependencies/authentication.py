from typing import HTTPException, Optional

from fastapi import Security
from fastapi.security import APIKeyHeader
from starlette import requests, status
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings

# from app.services.users import UserService
from app.resources import strings


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


# async def _get_current_user(
#     service: UserService = Depends(UserService),
#     token
# ):
#     pass
