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