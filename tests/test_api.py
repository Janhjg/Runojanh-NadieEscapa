# GET /crimes
def test_get_crimes_limite():
    crimes = get_crimes(archivo, limit=5)
    assert len(crimes) == 5

def test_get_crimes_offset():
    crimes = get_crimes(archivo, limit=3, offset=1)
    assert len(crimes) == 3

def test_get_crimes_limite_negativo():
    try:
        get_crimes(archivo, limit=-1)
        assert False
    except ValueError:
        assert True

def test_get_crimes_limite_cero():
    try:
        get_crimes(archivo, limit=0)
        assert False
    except ValueError:
        assert True

def test_get_crimes_limite_texto():
    try:
        get_crimes(archivo, limit="abc")
        assert False
    except ValueError:
        assert True





# GET /crimes/{id}
def test_get_crime_id_existente():
    crime = get_crime_by_id(archivo, 1)
    assert "id" in crime

def test_get_crime_id_no_existe():
    try:
        get_crime_by_id(archivo, 999999)
        assert False
    except ValueError:
        assert True

def test_get_crime_id_negativo():
    try:
        get_crime_by_id(archivo, -1)
        assert False
    except ValueError:
        assert True




# POST /predict/new
def test_predict_new_valido():
    res = predict_arrest(district="A", hora=10, mes=5, dia_de_semana=2, tipo="robo")
    assert res in [True, False]

def test_predict_new_falta_campo():
    try:
        predict_arrest(district="A", hora=10)
        assert False
    except ValueError:
        assert True

def test_district_invalido():
    try:
        predict_arrest(district="Z", hora=10, mes=5, dia_de_semana=2, tipo="robo")
        assert False
    except ValueError:
        assert True

def test_hora_fuera_rango():
    try:
        predict_arrest(district="A", hora=30, mes=5, dia_de_semana=2, tipo="robo")
        assert False
    except ValueError:
        assert True

def test_mes_fuera_rango():
    try:
        predict_arrest(district="A", hora=10, mes=20, dia_de_semana=2, tipo="robo")
        assert False
    except ValueError:
        assert True

def test_dia_fuera_rango():
    try:
        predict_arrest(district="A", hora=10, mes=5, dia_de_semana=9, tipo="robo")
        assert False
    except ValueError:
        assert True

def test_tipo_dato_incorrecto():
    try:
        predict_arrest(district="A", hora="diez", mes=5, dia_de_semana=2, tipo="robo")
        assert False
    except ValueError:
        assert True





# GET /predict/{id}
def test_predict_id_existente():
    res = predict_by_id(archivo, 1)
    assert "clase_predicha" in res

def test_predict_id_no_existe():
    try:
        predict_by_id(archivo, 999999)
        assert False
    except ValueError:
        assert True

def test_predict_id_negativo():
    try:
        predict_by_id(archivo, -1)
        assert False
    except ValueError:
        assert True

def test_predict_id_texto():
    try:
        predict_by_id(archivo, "abc")
        assert False
    except ValueError:
        assert True

def test_predict_id_cero():
    try:
        predict_by_id(archivo, 0)
        assert False
    except ValueError:
        assert True



# POST /classify
def test_classify_valido():
    etiqueta = classify_crime(crime_tipo="robo", district="A", clase_predicha="arrestado")
    assert isinstance(etiqueta, str)

def test_classify_falta_datos():
    try:
        classify_crime()
        assert False
    except ValueError:
        assert True

def test_classify_falta_prediccion():
    try:
        classify_crime(crime_tipo="robo")
        assert False
    except ValueError:
        assert True

def test_clase_invalida():
    try:
        classify_crime(crime_tipo="robo", district="A", clase_predicha="otra")
        assert False
    except ValueError:
        assert True





# POST /narrate
def test_narrate_valido():
    texto = narrate_crime(crime_tipo="robo", district="A", clase_predicha="arrestado", etiqueta="negativo")
    assert len(texto) > 0

def test_narrate_body_vacio():
    try:
        narrate_crime()
        assert False
    except ValueError:
        assert True

def test_narrate_falta_datos_crimen():
    try:
        narrate_crime(etiqueta="negativo")
        assert False
    except ValueError:
        assert True

def test_narrate_falta_prediccion():
    try:
        narrate_crime(crime_tipo="robo")
        assert False
    except ValueError:
        assert True

def test_narrate_etiqueta_invalida():
    try:
        narrate_crime(crime_tipo="robo", district="A", clase_predicha="arrestado", etiqueta="otra")
        assert False
    except ValueError:
        assert True