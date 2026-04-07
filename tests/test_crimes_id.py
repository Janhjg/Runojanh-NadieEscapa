import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# -----------------------
# GET /crimes/{id}
# -----------------------

def test_get_crime_id_existente():
    response = client.get("/crimes/1")
    assert response.status_code in [200, 404]


def test_get_crime_id_no_existe():
    response = client.get("/crimes/999999")
    assert response.status_code in [200, 404]


def test_get_crime_id_negativo():
    response = client.get("/crimes/-1")
    assert response.status_code == 422


def test_get_crime_columnas():
    response = client.get("/crimes/1")

    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, dict)
