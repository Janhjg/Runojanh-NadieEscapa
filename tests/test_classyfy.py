import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# -----------------------
# POST /classify
# -----------------------
def payload_valido():
    return {
        "crime_tipo": "robo",
        "district": "A",
        "clase_predicha": "arrestado"
    }

def test_classify_valido():
    payload = {
        "crime_tipo": "robo",
        "district": "A",
        "clase_predicha": "arrestado"
    }

    response = client.post("/classify", json=payload)
    assert response.status_code == 200

def test_classify_etiqueta_valida():
    response = client.post("/classify", json=payload_valido())
    assert response.status_code == 200

    data = response.json()
    assert "etiqueta" in data

    etiquetas_validas = ["positivo", "negativo", "neutro"]
    assert data["etiqueta"] in etiquetas_validas


def test_classify_score_mas_alto():
    response = client.post("/classify", json=payload_valido())
    data = response.json()

    assert "scores" in data
    assert "etiqueta" in data

    etiqueta = data["etiqueta"]
    scores = data["scores"]

    max_score = max(scores.values())
    assert scores[etiqueta] == max_score


def test_classify_texto_construido():
    response = client.post("/classify", json=payload_valido())
    data = response.json()

    assert "texto_construido" in data
    assert isinstance(data["texto_construido"], str)
    assert len(data["texto_construido"]) > 0


def test_classify_cambia_con_clase_predicha():
    payload1 = payload_valido()
    payload2 = payload_valido()

    payload2["clase_predicha"] = "no arrestado"

    res1 = client.post("/classify", json=payload1).json()
    res2 = client.post("/classify", json=payload2).json()

    assert res1["etiqueta"] != res2["etiqueta"]


def test_classify_mismo_tipo_distinto_distrito():
    payload1 = payload_valido()
    payload2 = payload_valido()

    payload2["district"] = "B"

    res1 = client.post("/classify", json=payload1).json()
    res2 = client.post("/classify", json=payload2).json()

    assert "etiqueta" in res1
    assert "etiqueta" in res2


def test_classify_body_vacio():
    response = client.post("/classify", json={})
    assert response.status_code == 422


def test_classify_falta_datos_crimen():
    payload = {
        "clase_predicha": "arrestado"
    }

    response = client.post("/classify", json=payload)
    assert response.status_code == 422


def test_classify_falta_prediccion():
    payload = {
        "crime_tipo": "robo",
        "district": "A"
    }

    response = client.post("/classify", json=payload)
    assert response.status_code == 422


def test_classify_clase_predicha_invalida():
    payload = payload_valido()
    payload["clase_predicha"] = "otra"

    response = client.post("/classify", json=payload)
    assert response.status_code == 422


def test_classify_error_servicio(monkeypatch):

    def mock_error(*args, **kwargs):
        raise Exception("HF caído")

    monkeypatch.setattr("main.classify", mock_error)

    response = client.post("/classify", json=payload_valido())

    assert response.status_code in [500, 503]