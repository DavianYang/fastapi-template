from datetime import datetime, timedelta
from typing import Dict

import jwt
from pydantic import ValidationError

from app.config import settings
from app.models.schemas.jwt import JWTMeta, JWTUser
from app.models.schemas.users import User


def create_jwt_token(
    *, jwt_content: Dict[str, str], secret_key: str, expires_delta: timedelta
):
    to_encode = jwt_content.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update(JWTMeta(exp=expire, sub=settings.JWT_SUBJECT).dict())
    return jwt.encode(to_encode, secret_key, algorithm=settings.ALGORITHM).decode()


def create_access_token_for_user(user: User, secret_key: str) -> str:
    return create_jwt_token(
        jwt_content=JWTUser(name=user.name).dict(),
        secret_key=secret_key,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def get_username_from_token(token: str, secret_key: str) -> str:
    try:
        return JWTUser(
            **jwt.decode(token, secret_key, algorithms=[settings.ALGORITHM])
        ).name
    except jwt.PyJWTError as decode_error:
        raise ValueError("unable to decode JWT token") from decode_error
    except ValidationError as validation_error:
        raise ValueError("malformed payload in token") from validation_error
