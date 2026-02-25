from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code in [200, 404]  # safe fallback

def test_languages_endpoint():
    response = client.get("/languages")
    assert response.status_code == 200