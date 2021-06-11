from os import environ, getenv
import warnings
from docker import libdocker
import pytest
from asgi_lifespan import LifespanManager
from uuid import uuid4
import alembic
from fastapi import FastAPI
from tests.testing_helpers import pull_image, ping_postgres

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
            detach=True
        )
        docker.start(container=container["Id"])
        inspection = docker.inspect_container(container["Id"])
        host = inspection["NetworkSettings"]["IPAddress"]

        dsn = f"postgres://postgres:postgres@{host}/postgres"

        try:
            ping_postgres(dsn)
            environ["DB_CONNECTION"] = dsn

            yield container
        finally:
            docker.kill(container["Id"])
            docker.remove_container(container["Id"])
    else:
        yield
        return


@pytest.fixture(autouse=True)
async def apply_migrations(postgres_server: None) -> None:
    alembic.config.main(argv=["upgrade", "head"])
    yield
    alembic.config.main(argv=["downgrade", "base"])


@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from app.main import get_application

    return get_application()


@pytest.fixture
async def initialized_app(app: FastAPI) -> FastAPI:
    async with LifespanManager(app):
        yield app
