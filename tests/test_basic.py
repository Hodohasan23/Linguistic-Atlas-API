from fastapi.testclient import TestClient
from app.main import app
from app.database import get_engine
from sqlmodel import SQLModel

from app.database import get_engine

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Linguistic Atlas API is running"}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_missing_api_key_returns_401():
    response = client.get("/languages")
    assert response.status_code == 401


def test_valid_api_key_returns_200():
    response = client.get("/languages", headers={"X-API-Key": "secret123"})
    assert response.status_code == 200


def test_language_sets_requires_auth():
    response = client.get("/language-sets")
    assert response.status_code in [401, 404]


def test_language_not_found():
    response = client.get("/languages/doesnotexist", headers={"X-API-Key": "secret123"})
    assert response.status_code == 404
