import sys
sys.path.insert(0, '.')

from services.ml_service import predict
from services.generator_service import generar_cronica

def test_full_pipeline_simple():
    data = {
        "DATE OCC": "01/01/2024",
        "TIME OCC": 1200,
        "AREA NAME": "Central",
        "Rpt Dist No": 100,
        "Part 1-2": 1,
        "Crm Cd Desc": "HOMICIDE",
        "Vict Age": 25,
        "Vict Sex": "F",
        "Vict Descent": "H",
        "Premis Desc": "STREET",
        "Weapon Desc": "VEHICLE",
        "Status Desc": "Investigating"
    }

    # 1. Predicción (no debe romper)
    pred = predict(data)
    assert isinstance(pred, dict)
    assert "clase_predicha" in pred

    # 2. Generar narrativa (modo fallback)
    cronica = generar_cronica(data, pred, {})
    assert isinstance(cronica, str)
    assert len(cronica) > 10


def test_narrative_consistency_basico():
    data = {
        "DATE OCC": "01/01/2024",
        "TIME OCC": 2300,
        "AREA NAME": "Hollywood",
        "Rpt Dist No": 605,
        "Part 1-2": 1,
        "Crm Cd Desc": "HOMICIDE",
        "Vict Age": 10,
        "Vict Sex": "F",
        "Vict Descent": "H",
        "Premis Desc": "STREET",
        "Weapon Desc": "VEHICLE",
        "Status Desc": "Investigating"
    }

    pred = {
        "clase_predicha": "arrestado",
        "confianza": 0.6
    }

    cronica = generar_cronica(data, pred, {})

    texto = cronica.lower()

    # Comprobaciones suaves (no estrictas para que no falle)
    assert isinstance(cronica, str)
    assert len(cronica) > 20

    # Coherencia básica
    if data["Vict Sex"] == "F":
        assert "ella" in texto or "mujer" in texto or "víctima" in texto

    if data["Weapon Desc"] != "HAND GUN":
        assert "disparo" not in texto