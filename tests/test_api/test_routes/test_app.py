from starlette import responses
from starlette.testclient import TestClient
from app.entrypoints.app import app

client = TestClient(app)

def test_api():
    response = client.get("/api/user")
    assert responses.status_code == 200
    assert responses.json() == {
        "Key": "Hello World"
    }