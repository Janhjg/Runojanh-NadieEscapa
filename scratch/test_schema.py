import os
import sys

sys.path.append(os.getcwd())
from schemas.full_case import FullCaseByIdOutput

datos_caso = {
    "DR_NO": 220109275,
    "DATE_OCC": "2023-01-01",
    "TIME_OCC": 1200,
    "AREA": 1,
    "AREA_NAME": "Central",
    "Rpt_Dist_No": 123,
    "Part_1_2": 1,
    "Crm_Cd": 123,
    "Crm_Cd_Desc": "ASSAULT",
    "Vict_Age": 30,
    "Vict_Sex": "M",
    "Vict_Descent": "B",
    "Premis_Cd": 123,
    "Premis_Desc": "STREET",
    "Weapon_Used_Cd": None,
    "Weapon_Desc": None,
    "Status_Desc": "IC",
    "Crm_Cd_2": None,
    "Crm_Cd_3": None,
    "Crm_Cd_4": None,
    "LOCATION": "123 STREET",
    "LAT": None,
    "LON": None,
}

prediccion_ml = {
    "clase_predicha": "arrestado",
    "probabilidad_arrestado": 0.8,
    "probabilidad_no_arrestado": 0.2,
    "confianza": 0.8,
    "modelo": "RF",
}

clasificacion_hf = {
    "etiqueta": {"labels_genericas": "frío y calculado"},
    "confianza": {"labels_genericas": 0.9},
    "texto_construido": "xyz",
    "todas_etiquetas": {"labels_genericas": [{"label": "x", "score": 1.0}]},
    "modelo": "BART"
}

try:
    obj = FullCaseByIdOutput(
        id=220109275,
        datos_caso=datos_caso,
        prediccion_ml=prediccion_ml,
        clasificacion_hf=clasificacion_hf,
        cronica="This is a test."
    )
    print("PYDANTIC VALIDATION SUCCESS!")
except Exception as e:
    import traceback
    traceback.print_exc()

