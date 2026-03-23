import pytest
from fastapi import HTTPException


# GET /crimes
def test_get_crimes_limite():
    crimes = get_crimes(archivo, limit=5)
    assert len(crimes) == 5


def test_get_crimes_cantidad_correcta():
    crimes = get_crimes(archivo, limit=3)
    assert len(crimes) == 3


def test_get_crimes_limite_mayor_total():
    total = len(archivo)
    with pytest.raises(HTTPException):
        get_crimes(archivo, limit=total + 1)


def test_get_crimes_limite_negativo():
    with pytest.raises(HTTPException):
        get_crimes(archivo, limit=-1)


def test_get_crimes_limite_cero():
    with pytest.raises(HTTPException):
        get_crimes(archivo, limit=0)


def test_get_crimes_limite_texto():
    with pytest.raises(HTTPException):
        get_crimes(archivo, limit="abc")


def test_get_crimes_offset():
    crimes = get_crimes(archivo, limit=3, offset=1)
    assert len(crimes) == 3


def test_get_crimes_offset_rango():
    crimes = get_crimes(archivo, limit=10, offset=10)

    for i in range(10):
        assert crimes[i]["id"] == archivo[10 + i]["id"]


def test_get_crimes_columnas():
    crimes = get_crimes(archivo, limit=1)

    columnas_correctas = {"id", "date", "district", "tipo"}
    assert set(crimes[0].keys()) == columnas_correctas


def test_get_crimes_fecha():
    fecha = "2023-01-01"
    crimes = get_crimes_by_date(archivo, fecha)

    for crime in crimes:
        assert crime["date"] == fecha


def test_get_crimes_rango_fechas():
    inicio = "2023-01-01"
    fin = "2023-01-31"

    crimes = get_crimes_by_date_range(archivo, inicio, fin)

    for crime in crimes:
        assert inicio <= crime["date"] <= fin

def test_get_crimes_cantidad_igual_limit():
    limit = 5
    crimes = get_crimes(archivo, limit=limit)
    
    assert len(crimes) == limit



# GET /crimes/{id}
def test_get_crime_id_existente():
    crime = get_crime_by_id(archivo, 1)
    assert "id" in crime
    columnas_esperadas = {"id", "date", "district", "tipo"}
    assert set(crime.keys()) == columnas_esperadas
    for columna in columnas_esperadas:
        assert crime[columna] is not None
        assert crime[columna] != ""


def test_get_crime_id_no_existe():
    with pytest.raises(HTTPException) as exc:
        get_crime_by_id(archivo, 999999)
    assert exc.value.status_code == 404
    assert exc.value.detail.get("error") == "NOT_FOUND"


def test_get_crime_id_negativo():
    with pytest.raises(HTTPException) as exc:
        get_crime_by_id(archivo, -1)

    assert exc.value.status_code == 400
    assert exc.value.detail.get("error") == "BAD_REQUEST"



# POST /predict/new
def test_predict_new_valido():
    res = predict_arrest(district="A", hora=10, mes=5, dia_de_semana=2, tipo="robo")
    assert isinstance(res, bool)


def test_predict_new_falta_campo():
    with pytest.raises(ValueError):
        predict_arrest(district="A", hora=10)


def test_district_invalido():
    with pytest.raises(ValueError):
        predict_arrest(district="Z", hora=10, mes=5, dia_de_semana=2, tipo="robo")


def test_hora_fuera_rango():
    with pytest.raises(ValueError):
        predict_arrest(district="A", hora=30, mes=5, dia_de_semana=2, tipo="robo")


def test_mes_fuera_rango():
    with pytest.raises(ValueError):
        predict_arrest(district="A", hora=10, mes=20, dia_de_semana=2, tipo="robo")


def test_dia_fuera_rango():
    with pytest.raises(ValueError):
        predict_arrest(district="A", hora=10, mes=5, dia_de_semana=9, tipo="robo")


def test_tipo_dato_incorrecto():
    with pytest.raises(ValueError):
        predict_arrest(district="A", hora="diez", mes=5, dia_de_semana=2, tipo="robo")



# GET /predict/{id}
def test_predict_id_existente():
    res = predict_by_id(archivo, 1)
    assert "clase_predicha" in res


def test_predict_id_no_existe():
    with pytest.raises(HTTPException):
        predict_by_id(archivo, 999999)


def test_predict_id_negativo():
    with pytest.raises(HTTPException):
        predict_by_id(archivo, -1)


def test_predict_id_texto():
    with pytest.raises(HTTPException):
        predict_by_id(archivo, "abc")


def test_predict_id_cero():
    with pytest.raises(HTTPException):
        predict_by_id(archivo, 0)



# POST /classify
def test_classify_valido():
    etiqueta = classify_crime(crime_tipo="robo", district="A", clase_predicha="arrestado")
    assert isinstance(etiqueta, str)


def test_classify_falta_datos():
    with pytest.raises(ValueError):
        classify_crime()


def test_classify_falta_prediccion():
    with pytest.raises(ValueError):
        classify_crime(crime_tipo="robo")


def test_clase_invalida():
    with pytest.raises(ValueError):
        classify_crime(crime_tipo="robo", district="A", clase_predicha="otra")



# POST /narrate
def test_narrate_valido():
    texto = narrate_crime(crime_tipo="robo", district="A", clase_predicha="arrestado", etiqueta="negativo")
    assert len(texto) > 0


def test_narrate_body_vacio():
    with pytest.raises(ValueError):
        narrate_crime()


def test_narrate_falta_datos_crimen():
    with pytest.raises(ValueError):
        narrate_crime(etiqueta="negativo")


def test_narrate_falta_prediccion():
    with pytest.raises(ValueError):
        narrate_crime(crime_tipo="robo")


def test_narrate_etiqueta_invalida():
    with pytest.raises(ValueError):
        narrate_crime(crime_tipo="robo", district="A", clase_predicha="arrestado", etiqueta="otra")