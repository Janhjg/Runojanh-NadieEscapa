import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# -----------------------
# POST /narrate
# -----------------------

def payload_valido():
    return {
        "crime_tipo": "robo",
        "district": "A",
        "clase_predicha": "arrestado",
        "etiqueta": "negativo"
    }


def test_narrate_valido():
    payload = {
        "crime_tipo": "robo",
        "district": "A",
        "clase_predicha": "arrestado",
        "etiqueta": "negativo"
    }

    response = client.post("/narrate", json=payload)
    assert response.status_code == 200

    def test_narrate_texto_no_vacio():
     response = client.post("/narrate", json=payload_valido())
    assert response.status_code == 200

    texto = response.json()
    assert texto is not None
    assert isinstance(texto, str)
    assert len(texto.strip()) > 0


def test_narrate_mas_100_palabras():
    response = client.post("/narrate", json=payload_valido())
    texto = response.json()

    assert len(texto.split()) > 100


def test_narrate_menciona_barrio():
    response = client.post("/narrate", json=payload_valido())
    texto = response.json()

    assert "A" in texto


def test_narrate_menciona_tipo_crimen():
    response = client.post("/narrate", json=payload_valido())
    texto = response.json()

    assert "robo" in texto.lower()


def test_narrate_respuestas_distintas():
    res1 = client.post("/narrate", json=payload_valido()).json()
    res2 = client.post("/narrate", json=payload_valido()).json()

    assert res1 != res2


def test_narrate_no_contiene_json_crudo():
    response = client.post("/narrate", json=payload_valido())
    texto = response.json()

    assert "probabilidad_arrestado" not in texto

def test_narrate_body_vacio():
    response = client.post("/narrate", json={})
    assert response.status_code == 422


def test_narrate_falta_datos_crimen():
    payload = {
        "clase_predicha": "arrestado",
        "etiqueta": "negativo"
    }

    response = client.post("/narrate", json=payload)
    assert response.status_code == 422


def test_narrate_falta_prediccion():
    payload = {
        "crime_tipo": "robo",
        "district": "A",
        "etiqueta": "negativo"
    }

    response = client.post("/narrate", json=payload)
    assert response.status_code == 422


def test_narrate_falta_etiqueta():
    payload = {
        "crime_tipo": "robo",
        "district": "A",
        "clase_predicha": "arrestado"
    }

    response = client.post("/narrate", json=payload)
    assert response.status_code == 422


def test_narrate_etiqueta_invalida():
    payload = {
        "crime_tipo": "robo",
        "district": "A",
        "clase_predicha": "arrestado",
        "etiqueta": "otra"
    }

    response = client.post("/narrate", json=payload)
    assert response.status_code == 422


def test_narrate_clase_predicha_invalida():
    payload = {
        "crime_tipo": "robo",
        "district": "A",
        "clase_predicha": "otra",
        "etiqueta": "negativo"
    }

    response = client.post("/narrate", json=payload)
    assert response.status_code == 422

def test_narrate_error_servicio(monkeypatch):

    def mock_error(*args, **kwargs):
        raise Exception("Fallo IA")

    monkeypatch.setattr("main.narrate", mock_error)

    response = client.post("/narrate", json=payload_valido())
    assert response.status_code in [500, 503]


def test_narrate_timeout(monkeypatch):

    def mock_timeout(*args, **kwargs):
        raise TimeoutError("Timeout")

    monkeypatch.setattr("main.narrate", mock_timeout)

    response = client.post("/narrate", json=payload_valido())
    assert response.status_code in [500, 504]