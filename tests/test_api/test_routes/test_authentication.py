import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from app.models.domain.users import User
from app.services.jwt import create_access_token_for_user

pytestmark = pytest.mark.asyncio


async def test_unable_to_login_with_jwt_prefix(
    app: FastAPI, client: AsyncClient, token: str
) -> None:
    response = await client.get(
        app.url_path_for("users:get-current-user"),
        headers={"Authorization": f"Wrong prefix {token}"},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_unable_login_when_user_does_no_exist_anymore(
    app: FastAPI, client: AsyncClient, authorization_prefix: str
) -> None:
    token = create_access_token_for_user(
        User(name="user", email="email@email.com"), "secret"
    )
    response = await client.get(
        app.url_path_for("users:get-current-user"),
        headers={"Authorization": f"{authorization_prefix} {token}"},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
