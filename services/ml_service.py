import joblib
import pandas as pd
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
ML_DIR = BASE_DIR / "models"

pipeline_model = None

MODEL_PATH = ML_DIR / "crime_data_model.pkl"

if os.path.exists(MODEL_PATH):
    pipeline_model = joblib.load(MODEL_PATH)

encoderVictSex = joblib.load(ML_DIR / "encoder_VictSex.joblib")
encoderVictDescent = joblib.load(ML_DIR / "encoder_VictDescent.joblib")
mapper_area = pd.read_csv(ML_DIR / "mapper_area.csv")
mapper_crm = pd.read_csv(ML_DIR / "mapper_crm.csv")
mapper_premis = pd.read_csv(ML_DIR / "mapper_premis.csv")
mapper_weapon = pd.read_csv(ML_DIR / "mapper_weapon.csv")


def prepare_features(data: dict) -> pd.DataFrame:
    fecha = pd.to_datetime(data.get("DATE OCC"), errors="coerce")

    año = fecha.year if not pd.isna(fecha) else 0
    mes = fecha.month if not pd.isna(fecha) else 0
    dia = fecha.day if not pd.isna(fecha) else 0

    Vict_Sex = (
        encoderVictSex.transform([data["Vict Sex"]])[0]
        if data.get("Vict Sex") in encoderVictSex.classes_
        else -1
    )

    Vict_Descent = (
        encoderVictDescent.transform([data["Vict Descent"]])[0]
        if data.get("Vict Descent") in encoderVictDescent.classes_
        else -1
    )

    def map_value(df, col, value, target):
        if value is None or value not in df[col].values:
            return 0
        return int(df[df[col] == value][target].iloc[0])

    areaCode = map_value(mapper_area, "AREA NAME", data.get("AREA NAME"), "AREA")
    Crm1Code = map_value(mapper_crm, "Crm Cd Desc", data.get("Crm Cd Desc"), "Crm Cd")

    def crm_extra(key):
        val = data.get(key)
        return map_value(mapper_crm, "Crm Cd Desc", val, "Crm Cd")

    Crm2Code = crm_extra("Crm Cd 2 Desc")
    Crm3Code = crm_extra("Crm Cd 3 Desc")
    Crm4Code = crm_extra("Crm Cd 4 Desc")

    premisCode = map_value(mapper_premis, "Premis Desc", data.get("Premis Desc"), "Premis Cd")
    weaponCode = map_value(mapper_weapon, "Weapon Desc", data.get("Weapon Desc"), "Weapon Used Cd")

    return pd.DataFrame([{
        "TIME OCC": data.get("TIME OCC", 0),
        "AREA": areaCode,
        "Rpt Dist No": data.get("Rpt Dist No", 0),
        "Part 1-2": data.get("Part 1-2", 0),
        "Crm Cd": Crm1Code,
        "Vict Age": data.get("Vict Age", 0),
        "Vict Sex": Vict_Sex,
        "Vict Descent": Vict_Descent,
        "Premis Cd": premisCode,
        "Weapon Used Cd": weaponCode,
        "Crm Cd 2": Crm2Code,
        "Crm Cd 3": Crm3Code,
        "Crm Cd 4": Crm4Code,
        "YEAR OCC": año,
        "MONTH OCC": mes,
        "DAY OCC": dia
    }])


def predict(data: dict) -> dict:
    if pipeline_model is None:
        return {
            "clase_predicha": "mock",
            "probabilidad_arrestado": 0.5,
            "probabilidad_no_arrestado": 0.5,
            "confianza": 0.5,
            "modelo": "mock-model"
        }

    X = prepare_features(data)

    clase_idx = pipeline_model.predict(X)[0]
    probs = pipeline_model.predict_proba(X)[0]

    return {
        "clase_predicha": "arrestado" if clase_idx == 1 else "no arrestado",
        "probabilidad_arrestado": round(float(probs[1]), 4),
        "probabilidad_no_arrestado": round(float(probs[0]), 4),
        "confianza": round(float(max(probs)), 4),
        "modelo": "RandomForestClassifier"
    }