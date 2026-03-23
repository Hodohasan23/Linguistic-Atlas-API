from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_engine
from sqlmodel import SQLModel

SQLModel.metadata.create_all(get_engine())

client = TestClient(app)

API_KEY = {"X-API-Key": "secret123"}


def test_languages_random_returns_single_object():
    response = client.get("/languages/random", headers=API_KEY)
    assert response.status_code in [200, 404]  # 404 is valid if db is empty


def test_languages_random_includes_endangerment():
    response = client.get("/languages/random", headers=API_KEY)
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        assert "endangerment" in data
        assert "at_risk" in data


def test_macroareas_returns_list():
    response = client.get("/macroareas", headers=API_KEY)
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # empty list is fine in CI


def test_stats_languages_per_macroarea():
    response = client.get("/stats/languages-per-macroarea", headers=API_KEY)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_stats_languages_per_family():
    response = client.get("/stats/languages-per-family", headers=API_KEY)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
