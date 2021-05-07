from starlette.testclient import TestClient

from app.entrypoints.app import app

client = TestClient(app)


def test_api():
    response = client.get("/api/user")
    assert response.status_code == 200
    assert response.json() == {"Key": "Hello World"}
