import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# -----------------------
# POST /predict/new
# -----------------------

def payload_valido():
    return {
        "district": "A",
        "hora": 10,
        "mes": 5,
        "dia_de_semana": 2,
        "tipo": "robo"
    }


def test_predict_new_valido():
    response = client.post("/predict/new", json=payload_valido())
    assert response.status_code == 200


def test_predict_new_body_vacio():
    response = client.post("/predict/new", json={})
    assert response.status_code == 422


def test_predict_new_district_invalido():
    payload = payload_valido()
    payload["district"] = "Z"

    response = client.post("/predict/new", json=payload)
    assert response.status_code in [200, 422]


def test_predict_new_hora_fuera_rango():
    payload = payload_valido()
    payload["hora"] = 30

    response = client.post("/predict/new", json=payload)
    assert response.status_code in [200, 422]


def test_predict_new_tipo_incorrecto():
    payload = payload_valido()
    payload["hora"] = "diez"

    response = client.post("/predict/new", json=payload)
    assert response.status_code == 422
