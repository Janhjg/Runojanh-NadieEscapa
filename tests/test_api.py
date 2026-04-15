import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# =====================================================
# HOME + STATUS
# =====================================================

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "nombre" in response.json()


def test_status():
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# =====================================================
# GET /crimes
# =====================================================

def test_get_crimes_ok():
    response = client.get("/crimes?limit=5")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)


def test_get_crimes_limit_invalid():
    response = client.get("/crimes?limit=0")
    assert response.status_code == 422


def test_get_crimes_offset_invalid():
    response = client.get("/crimes?offset=-1")
    assert response.status_code == 422


def test_get_crimes_offset():
    response = client.get("/crimes?limit=5&offset=10")
    assert response.status_code == 200


# =====================================================
# GET /crimes/{id}
# =====================================================

def test_get_crime_by_id_ok():
    response = client.get("/crimes/1")
    assert response.status_code in [200, 404]


def test_get_crime_by_id_invalid():
    response = client.get("/crimes/-1")
    assert response.status_code == 422


def test_get_crime_by_id_text():
    response = client.get("/crimes/abc")
    assert response.status_code == 422


# =====================================================
# POST /predict/new
# =====================================================

def predict_payload():
    return {
        "district": "A",
        "hora": 10,
        "mes": 5,
        "dia_de_semana": 2,
        "tipo": "robo"
    }


def test_predict_new():
    response = client.post("/predict/new", json=predict_payload())
    assert response.status_code in [200, 503]


def test_predict_new_empty():
    response = client.post("/predict/new", json={})
    assert response.status_code == 422


# =====================================================
# GET /predict/{id}
# =====================================================

def test_predict_by_id():
    response = client.get("/predict/1")
    assert response.status_code in [200, 404, 400]


def test_predict_by_id_invalid():
    response = client.get("/predict/-1")
    assert response.status_code == 422


def test_predict_by_id_text():
    response = client.get("/predict/abc")
    assert response.status_code == 422


# =====================================================
# POST /classify
# =====================================================

def classify_payload():
    return {
        "crime_tipo": "robo",
        "district": "A",
        "clase_predicha": "arrestado"
    }


def test_classify():
    response = client.post("/classify", json=classify_payload())
    assert response.status_code == 200


def test_classify_empty():
    response = client.post("/classify", json={})
    assert response.status_code == 422


# =====================================================
# POST /narrate
# =====================================================

def narrate_payload():
    return {
        "crime_tipo": "robo",
        "district": "A",
        "clase_predicha": "arrestado",
        "etiqueta": "negativo"
    }


def test_narrate():
    response = client.post("/narrate", json=narrate_payload())
    assert response.status_code in [200, 500, 503]


def test_narrate_empty():
    response = client.post("/narrate", json={})
    assert response.status_code == 422