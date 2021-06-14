import warnings
from os import getenv
from uuid import uuid4

# import alembic.config
import docker as libdocker
import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient

from api.services import jwt
from app.config import settings
from app.models.domain.users import UserInDB
from app.services.users import UserService
from tests.testing_helpers import ping_postgres, pull_image

POSTGRES_DOCKER_IMAGE = "postgres:11.4-alpine"

USE_LOCAL_DB = getenv("USE_LOCAL_DB_FOR_TEST", False)


@pytest.fixture(scope="session")
def docker() -> libdocker.APIClient:
    with libdocker.APIClient(version="auto") as client:
        yield client


@pytest.fixture(scope="session")
def postgres_server(docker: libdocker.APIClient) -> None:
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    if not USE_LOCAL_DB:
        pull_image(docker, POSTGRES_DOCKER_IMAGE)

        container = docker.create_container(
            image=POSTGRES_DOCKER_IMAGE,
            name="test-postgres-{}".format(uuid4()),
            detach=True,
        )
        docker.start(container=container["Id"])
        inspection = docker.inspect_container(container["Id"])
        host = inspection["NetworkSettings"]["IPAddress"]

        dsn = f"postgresql://postgres:postgres@{host}/postgres"

        try:
            ping_postgres(dsn)
            settings.DB_CONNECTION = dsn

            yield container
        finally:
            docker.kill(container["Id"])
            docker.remove_container(container["Id"])
    else:
        yield
        return


@pytest.fixture
def app(postgres_server: None) -> FastAPI:
    from app.main import get_application

    return get_application()


@pytest.fixture
async def initialized_app(app: FastAPI) -> FastAPI:
    async with LifespanManager(app):
        yield app


@pytest.fixture
async def client(initialized_app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=initialized_app,
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest.fixture
def authorization_prefix() -> str:
    from app.config import settings

    return settings.JWT_TOKEN_PREFIX


@pytest.fixture
async def test_user() -> UserInDB:
    user_service = UserService()
    return await user_service.create_user(
        email="test@test.com", password="password", name="testuser"
    )


@pytest.fixture
def token(test_user: UserInDB) -> str:
    return jwt.create_access_token_for_user(test_user, settings.SECRET_KEY)


@pytest.fixture
def authorized_client(
    client: AsyncClient, token: str, authorization_prefix: str
) -> AsyncClient:
    client.headers = {
        "Authorization": f"{authorization_prefix} {token}",
        **client.headers,
    }

    return client
