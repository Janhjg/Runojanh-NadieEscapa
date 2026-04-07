import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# -----------------------
# GET /crimes
# -----------------------

def test_get_crimes_cantidad_correcta():
    response = client.get("/crimes?limit=5")
    assert response.status_code == 200


def test_get_crimes_limit_mayor_total():
    response = client.get("/crimes?limit=999999")
    assert response.status_code == 200  # aún no validas esto


def test_get_crimes_limit_negativo():
    response = client.get("/crimes?limit=-1")
    assert response.status_code == 422


def test_get_crimes_limit_cero():
    response = client.get("/crimes?limit=0")
    assert response.status_code == 422


def test_get_crimes_limit_texto():
    response = client.get("/crimes?limit=abc")
    assert response.status_code == 422


def test_get_crimes_offset():
    response = client.get("/crimes?limit=5&offset=10")
    assert response.status_code == 200