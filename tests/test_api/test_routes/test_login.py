import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.status import HTTP_200_OK

from app.models.domain.users import UserInDB


pytestmark = pytest.mark.asyncio


async def test_user_successful_login(app: FastAPI, client: AsyncClient, test_user: UserInDB) -> None:
    login_json = {
        "user": {
            "email": "test@test.com",
            "password": "password"
        }
    }

    response = await client.post(app.url_path_for("auth:login"), json=login_json)
    assert response.status_code == HTTP_200_OK
