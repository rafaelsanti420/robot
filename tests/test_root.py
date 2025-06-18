from fastapi.testclient import TestClient
from api_gateway.app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "api_gateway"}


def test_ui():
    response = client.get("/ui")
    assert response.status_code == 200
    assert b"Robot Services" in response.content
