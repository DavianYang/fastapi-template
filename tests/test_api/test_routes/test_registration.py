import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from app.models.domain.users import UserInDB

pytestmark = pytest.mark.asyncio


def create_registration_user_demo():
    email, name, password = "test@test.com", "username", "password"
    return {"user": {"email": email, "name": name, "password": password}}


async def test_user_success_registration(app: FastAPI, client: AsyncClient) -> None:
    registration_json = create_registration_user_demo()
    response = await client.post(
        app.url_path_for("auth:register"), json=registration_json
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.parametrize(
    "credentials_part, credentials_value",
    (("name", "free_username"), ("email", "free-email@gmail.com")),
)
async def test_failed_user_registration_when_some_credentials_are_taken(
    app: FastAPI,
    client: AsyncClient,
    test_user: UserInDB,
    credentials_part: str,
    credentials_value: str,
) -> None:
    registration_json = create_registration_user_demo()
    registration_json["user"][credentials_part] == credentials_value

    response = await client.post(
        app.url_path_for("auth:register"), json=registration_json
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
