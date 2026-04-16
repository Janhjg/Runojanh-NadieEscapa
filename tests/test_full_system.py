import pytest
from services.ml_service import predict


def test_predict_mock_or_real():
    # Caso mínimo válido según tu prepare_features
    fake_input = {
        "DATE OCC": "2023-01-01",
        "TIME OCC": 1200,
        "AREA NAME": "Central",
        "Rpt Dist No": 123,
        "Part 1-2": 1,
        "Crm Cd Desc": "THEFT",
        "Vict Age": 30,
        "Vict Sex": "M",
        "Vict Descent": "H",
        "Premis Desc": "STREET",
        "Weapon Desc": None,
        "Crm Cd 2 Desc": None,
        "Crm Cd 3 Desc": None,
        "Crm Cd 4 Desc": None
    }

    result = predict(fake_input)

    # validaciones básicas
    assert isinstance(result, dict)
    assert "clase_predicha" in result
    assert "confianza" in result
    assert result["clase_predicha"] in ["arrestado", "no arrestado", "mock"]