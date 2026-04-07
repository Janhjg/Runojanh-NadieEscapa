import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# -----------------------
# GET /predict/{id}
# -----------------------

def test_predict_id_existente():
    response = client.get("/predict/1")
    assert response.status_code in [200, 404]


def test_predict_id_no_existe():
    response = client.get("/predict/999999")
    assert response.status_code in [200, 404]


def test_predict_id_negativo():
    response = client.get("/predict/-1")
    assert response.status_code == 422


def test_predict_id_texto():
    response = client.get("/predict/abc")
    assert response.status_code == 422


def test_predict_id_cero():
    response = client.get("/predict/0")
    assert response.status_code == 422


def test_predict_clase_predicha_valida():
    response = client.get("/predict/1")

    if response.status_code == 200:
        data = response.json()
        if "clase_predicha" in data:
            assert data["clase_predicha"] in ["arrestado", "no arrestado"]

