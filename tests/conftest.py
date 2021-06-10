import pytest
from fastapi import FastAPI


@pytest.fixture
def app() -> FastAPI:
    from app.main import get_application

    return get_application()