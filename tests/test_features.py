from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_engine
from sqlmodel import SQLModel

SQLModel.metadata.create_all(get_engine())

client = TestClient(app)

API_KEY = {"X-API-Key": "secret123"}


def get_token():
    client.post(
        "/auth/register",
        json={"email": "newuser@test.com", "password": "testpassword123"},
        headers=API_KEY,
    )
    response = client.post(
        "/auth/login",
        json={"email": "newuser@test.com", "password": "testpassword123"},
        headers=API_KEY,
    )
    return response.json().get("access_token", "")


def get_admin_token():
    client.post(
        "/auth/register",
        json={"email": "adminuser@test.com", "password": "testpassword123"},
        headers=API_KEY,
    )
    response = client.post(
        "/auth/login",
        json={"email": "adminuser@test.com", "password": "testpassword123"},
        headers=API_KEY,
    )
    return response.json().get("access_token", "")


# -----------------------
# Languages — new endpoints
# -----------------------


def test_languages_search_includes_endangerment():
    response = client.get("/languages/search?name=Somali", headers=API_KEY)
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        if data:
            assert "endangerment" in data[0]
            assert "at_risk" in data[0]


def test_languages_browse_includes_endangerment():
    response = client.get("/languages?limit=1", headers=API_KEY)
    assert response.status_code == 200
    data = response.json()
    if data:
        assert "endangerment" in data[0]


def test_languages_iso_lookup():
    response = client.get("/languages/iso/som", headers=API_KEY)
    assert response.status_code in [200, 404]


def test_languages_iso_invalid_returns_404():
    response = client.get("/languages/iso/zzz", headers=API_KEY)
    assert response.status_code == 404


def test_language_classification_returns_list():
    response = client.get("/languages/random", headers=API_KEY)
    if response.status_code == 200:
        language_id = response.json()["id"]
        classification_response = client.get(
            f"/languages/{language_id}/classification", headers=API_KEY
        )
        assert classification_response.status_code == 200
        data = classification_response.json()
        assert "classification" in data
        assert isinstance(data["classification"], list)


def test_language_names_endpoint():
    response = client.get("/languages/random", headers=API_KEY)
    if response.status_code == 200:
        language_id = response.json()["id"]
        names_response = client.get(f"/languages/{language_id}/names", headers=API_KEY)
        assert names_response.status_code in [200, 404]


def test_language_parameters_endpoint():
    response = client.get("/languages/random", headers=API_KEY)
    if response.status_code == 200:
        language_id = response.json()["id"]
        params_response = client.get(
            f"/languages/{language_id}/parameters", headers=API_KEY
        )
        assert params_response.status_code in [200, 404]


def test_language_endangerment_endpoint():
    response = client.get("/languages/random", headers=API_KEY)
    if response.status_code == 200:
        language_id = response.json()["id"]
        end_response = client.get(
            f"/languages/{language_id}/endangerment", headers=API_KEY
        )
        assert end_response.status_code == 200
        data = end_response.json()
        assert "status" in data
        assert "risk_summary" in data
        assert "years_since_last_study" in data
        assert "documentation_status" in data


def test_language_endangerment_invalid_id():
    response = client.get("/languages/doesnotexist/endangerment", headers=API_KEY)
    assert response.status_code == 404


# -----------------------
# Families
# -----------------------


def test_families_returns_list():
    response = client.get("/families", headers=API_KEY)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_families_all_have_family_level():
    response = client.get("/families?limit=10", headers=API_KEY)
    assert response.status_code == 200
    for family in response.json():
        assert family["level"].lower() == "family"


def test_family_invalid_id_returns_404():
    response = client.get("/families/doesnotexist", headers=API_KEY)
    assert response.status_code == 404


def test_family_languages_endpoint():
    families = client.get("/families?limit=1", headers=API_KEY).json()
    if families:
        family_id = families[0]["id"]
        response = client.get(f"/families/{family_id}/languages", headers=API_KEY)
        assert response.status_code == 200
        assert isinstance(response.json(), list)


# -----------------------
# Macroareas
# -----------------------


def test_macroareas_have_macroarea_field():
    response = client.get("/macroareas", headers=API_KEY)
    assert response.status_code == 200
    for item in response.json():
        assert "macroarea" in item


def test_macroarea_languages_africa():
    response = client.get("/macroareas/Africa/languages", headers=API_KEY)
    assert response.status_code in [200, 404]


def test_macroarea_languages_invalid_returns_404():
    response = client.get("/macroareas/doesnotexist/languages", headers=API_KEY)
    assert response.status_code == 404


# -----------------------
# Stats
# -----------------------


def test_stats_endangerment_breakdown():
    response = client.get("/stats/endangerment-breakdown", headers=API_KEY)
    assert response.status_code == 200
    data = response.json()
    assert "total_with_aes_data" in data
    assert "breakdown" in data
    assert "at_risk_total" in data
    assert isinstance(data["breakdown"], dict)


def test_stats_underdocumented():
    response = client.get("/stats/underdocumented", headers=API_KEY)
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert "languages" in data
    assert isinstance(data["languages"], list)


def test_stats_underdocumented_custom_year():
    response = client.get("/stats/underdocumented?before=1950", headers=API_KEY)
    assert response.status_code == 200
    data = response.json()
    assert data["threshold_year"] == 1950
    for lang in data["languages"]:
        assert lang["last_documented"] < 1950


def test_stats_underdocumented_languages_have_years_of_silence():
    response = client.get("/stats/underdocumented?before=1970", headers=API_KEY)
    assert response.status_code == 200
    for lang in response.json()["languages"]:
        assert "years_of_silence" in lang
        assert lang["years_of_silence"] > 0


# -----------------------
# Testimonies
# -----------------------


def test_testimonies_list_is_public():
    response = client.get("/language-sets", headers=API_KEY)
    assert response.status_code == 200


def test_create_testimony_requires_jwt():
    response = client.post(
        "/language-sets",
        json={"title": "Test", "description": "desc"},
        headers=API_KEY,
    )
    assert response.status_code in [401, 403, 422]


def test_create_and_retrieve_testimony():
    token = get_token()
    create = client.post(
        "/language-sets",
        json={"title": "Test Testimony", "description": "A test"},
        headers={**API_KEY, "Authorization": f"Bearer {token}"},
    )
    assert create.status_code in [200, 201]
    set_id = create.json()["id"]

    retrieve = client.get(f"/language-sets/{set_id}", headers=API_KEY)
    assert retrieve.status_code == 200
    assert retrieve.json()["title"] == "Test Testimony"


def test_add_invalid_language_to_testimony():
    token = get_token()
    create = client.post(
        "/language-sets",
        json={"title": "Lang Test"},
        headers={**API_KEY, "Authorization": f"Bearer {token}"},
    )
    set_id = create.json()["id"]

    response = client.post(
        f"/language-sets/{set_id}/languages",
        json={"language_id": "doesnotexist"},
        headers=API_KEY,
    )
    assert response.status_code == 404


def test_testimony_insights_empty():
    token = get_token()
    create = client.post(
        "/language-sets",
        json={"title": "Empty Testimony"},
        headers={**API_KEY, "Authorization": f"Bearer {token}"},
    )
    set_id = create.json()["id"]

    response = client.get(f"/language-sets/{set_id}/insights", headers=API_KEY)
    assert response.status_code == 200
    data = response.json()
    assert data["language_count"] == 0


def test_testimony_insights_invalid_id():
    response = client.get("/language-sets/999999/insights", headers=API_KEY)
    assert response.status_code == 404


def test_update_testimony():
    token = get_token()
    create = client.post(
        "/language-sets",
        json={"title": "Original Title"},
        headers={**API_KEY, "Authorization": f"Bearer {token}"},
    )
    set_id = create.json()["id"]

    update = client.patch(
        f"/language-sets/{set_id}",
        json={"title": "Updated Title"},
        headers=API_KEY,
    )
    assert update.status_code == 200
    assert update.json()["title"] == "Updated Title"


def test_testimony_not_found():
    response = client.get("/language-sets/999999", headers=API_KEY)
    assert response.status_code == 404


# -----------------------
# Analytics
# -----------------------


def test_analytics_similarity_same_language():
    response = client.get(
        "/analytics/similarity?lang1=stan1293&lang2=stan1293", headers=API_KEY
    )
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        assert "similarity_score" in data
        assert "insight" in data


def test_analytics_similarity_response_shape():
    response = client.get(
        "/analytics/similarity?lang1=stan1293&lang2=stan1295", headers=API_KEY
    )
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        assert "language1" in data
        assert "language2" in data
        assert "similarity_score" in data
        assert "explanation" in data


def test_analytics_outliers_returns_count():
    response = client.get("/analytics/outliers", headers=API_KEY)
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert "outliers" in data
    assert isinstance(data["outliers"], list)


def test_analytics_lineage_invalid_id():
    response = client.get("/analytics/lineage/doesnotexist", headers=API_KEY)
    assert response.status_code == 404


def test_analytics_lineage_valid():
    response = client.get("/languages/random", headers=API_KEY)
    if response.status_code == 200:
        language_id = response.json()["id"]
        lineage = client.get(f"/analytics/lineage/{language_id}", headers=API_KEY)
        assert lineage.status_code == 200
        data = lineage.json()
        assert "lineage" in data
        assert isinstance(data["lineage"], list)


def test_analytics_coverage_invalid_id():
    response = client.get("/analytics/coverage/doesnotexist", headers=API_KEY)
    assert response.status_code == 404


def test_analytics_coverage_valid():
    response = client.get("/languages/random", headers=API_KEY)
    if response.status_code == 200:
        language_id = response.json()["id"]
        coverage = client.get(f"/analytics/coverage/{language_id}", headers=API_KEY)
        assert coverage.status_code == 200
        data = coverage.json()
        assert "coverage_score" in data
        assert "parameter_count" in data
        assert "total_parameters" in data


def test_analytics_map_returns_coordinates():
    response = client.get("/languages/map?limit=5", headers=API_KEY)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "Latitude" in data[0]
        assert "Longitude" in data[0]
        assert "ID" in data[0]
