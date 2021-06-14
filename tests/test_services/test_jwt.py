from datetime import timedelta

import jwt
import pytest

from app.config import settings
from app.services.jwt import create_jwt_token, get_username_from_token


def test_creating_jwt_token() -> None:
    token = create_jwt_token(
        jwt_content={"content": "payload"},
        secret_key="secret",
        expires_delta=timedelta(minutes=1),
    )
    parsed_payload = jwt.decode(token, "secret", algorithms=[settings.ALGORITHM])

    assert parsed_payload["content"] == "payload"


def test_error_when_wrong_token() -> None:
    with pytest.raises(ValueError):
        get_username_from_token("asdf", "asdf")


def test_error_when_wrong_token_shape() -> None:
    token = create_jwt_token(
        jwt_content={"content": "payload"},
        secret_key="secret",
        expires_delta=timedelta(minutes=1),
    )
    with pytest.raises(ValueError):
        get_username_from_token(token, "secret")
