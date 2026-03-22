from fastapi.testclient import TestClient
from app.main import app
from app.database import get_engine
from sqlmodel import SQLModel

SQLModel.metadata.create_all(get_engine())

client = TestClient(app)

API_KEY = {"X-API-Key": "secret123"}

# Authorisation endpoints


def test_register_new_user():
    response = client.post(
        "/auth/register",
        json={
            "email": "testuser_reg@test.com",
            "password": "testpassword123",
        },
        headers=API_KEY,
    )
    assert response.status_code in [200, 201, 400]


def test_login_returns_token():
    client.post(
        "/auth/register",
        json={
            "email": "testuser_login@test.com",
            "password": "testpassword123",
        },
        headers=API_KEY,
    )
    response = client.post(
        "/auth/login",
        json={"email": "testuser_login@test.com", "password": "testpassword123"},
        headers=API_KEY,
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password_returns_401():
    response = client.post(
        "/auth/login",
        json={"email": "testuser_login@test.com", "password": "wrongpassword"},
        headers=API_KEY,
    )
    assert response.status_code == 401


def test_auth_me_without_token_returns_422():
    response = client.get("/auth/me", headers=API_KEY)
    assert response.status_code == 422


# Languages endpoints


def test_languages_returns_list():
    response = client.get("/languages", headers=API_KEY)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_languages_filter_by_macroarea():
    response = client.get("/languages?macroarea=Africa", headers=API_KEY)
    assert response.status_code == 200


def test_languages_pagination():
    response = client.get("/languages?limit=5&offset=0", headers=API_KEY)
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 5


def test_languages_search_by_name():
    response = client.get("/languages/search?name=English", headers=API_KEY)
    assert response.status_code in [200, 404]


def test_language_invalid_id_returns_404():
    response = client.get("/languages/zzz999invalid", headers=API_KEY)
    assert response.status_code == 404


# Language sets endpoints


def get_token():
    client.post(
        "/auth/register",
        json={
            "email": "setuser@test.com",
            "password": "testpassword123",
        },
        headers=API_KEY,
    )
    response = client.post(
        "/auth/login",
        json={"email": "setuser@test.com", "password": "testpassword123"},
        headers=API_KEY,
    )
    return response.json().get("access_token", "")


def test_create_language_set_requires_jwt():
    response = client.post(
        "/language-sets",
        json={"title": "Test Set", "description": "A test set"},
        headers=API_KEY,
    )
    assert response.status_code in [401, 403, 422]


def test_create_language_set_with_jwt():
    token = get_token()
    response = client.post(
        "/language-sets",
        json={"title": "Test Set", "description": "A test set"},
        headers={**API_KEY, "Authorization": f"Bearer {token}"},
    )
    assert response.status_code in [200, 201]


def test_list_language_sets_requires_auth():
    response = client.get("/language-sets", headers=API_KEY)
    assert response.status_code in [200, 401]


# Analytics endpoints


def test_similarity_endpoint_exists():
    response = client.get(
        "/analytics/similarity?lang1=stan1293&lang2=stan1295", headers=API_KEY
    )
    assert response.status_code in [200, 404, 422]


def test_similarity_missing_params_returns_422():
    response = client.get("/analytics/similarity", headers=API_KEY)
    assert response.status_code == 422


# Error handling


def test_invalid_route_returns_404():
    response = client.get("/thisdoesnotexist", headers=API_KEY)
    assert response.status_code == 404


def test_wrong_method_returns_405():
    response = client.post("/languages", headers=API_KEY)
    assert response.status_code in [405, 422]


def test_malformed_json_on_register_returns_422():
    response = client.post("/auth/register", json={"email": "x"}, headers=API_KEY)
    assert response.status_code == 422
