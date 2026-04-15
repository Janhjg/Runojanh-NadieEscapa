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
    data = response.json()
    assert "nombre" in data


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
    # 🔥 tu API ahora devuelve dict, no list
    assert isinstance(data, dict)
    assert "crimes" in data


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
# (AJUSTADO A TU SCHEMA REAL)
# =====================================================

def predict_payload():
    return {
        "DATE_OCC": "2023-01-01",
        "TIME_OCC": 1200,
        "AREA_NAME": "Central",
        "Rpt_Dist_No": 101,
        "Part_1_2": 1,
        "Crm_Cd_Desc": "ROBBERY",
        "Vict_Age": 30,
        "Vict_Sex": "M",
        "Vict_Descent": "H",
        "Premis_Desc": "STREET",
        "Weapon_Desc": None,
        "Crm_Cd_2_Desc": None,
        "Crm_Cd_3_Desc": None,
        "Crm_Cd_4_Desc": None
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
        "datos_crimen": {
            "DATE_OCC": "2023-01-01",
            "TIME_OCC": 1200,
            "AREA_NAME": "Central",
            "Rpt_Dist_No": 101,
            "Part_1_2": 1,
            "Crm_Cd_Desc": "ROBBERY",
            "Vict_Age": 30,
            "Vict_Sex": "M",
            "Vict_Descent": "H",
            "Premis_Desc": "STREET",
            "Weapon_Desc": None,
            "Crm_Cd_2_Desc": None,
            "Crm_Cd_3_Desc": None,
            "Crm_Cd_4_Desc": None
        },
        "prediccion_ml": {
            "clase_predicha": "arrestado"
        }
    }



def test_classify_empty():
    response = client.post("/classify", json={})
    assert response.status_code == 422


# =====================================================
# POST /narrate
# =====================================================

def narrate_payload():
    return {
        "datos_crimen": {
            "DATE_OCC": "2023-01-01",
            "TIME_OCC": 1200,
            "AREA_NAME": "Central",
            "Rpt_Dist_No": 101,
            "Part_1_2": 1,
            "Crm_Cd_Desc": "ROBBERY",
            "Vict_Age": 30,
            "Vict_Sex": "M",
            "Vict_Descent": "H",
            "Premis_Desc": "STREET",
            "Weapon_Desc": None,
            "Crm_Cd_2_Desc": None,
            "Crm_Cd_3_Desc": None,
            "Crm_Cd_4_Desc": None
        },
        "prediccion_ml": {
            "clase_predicha": "arrestado",
            "confianza": 0.8
        },
        "etiquetas_huggingface": {
            "positiva": 0.2,
            "negativa": 0.8
        }
    }



def test_narrate_empty():
    response = client.post("/narrate", json={})
    assert response.status_code == 422