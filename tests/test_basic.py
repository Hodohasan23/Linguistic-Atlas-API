from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_languages_endpoint():
    response = client.get(
        "/languages",
        headers={"X-API-Key": "secret123"}
    )
    assert response.status_code == 200
