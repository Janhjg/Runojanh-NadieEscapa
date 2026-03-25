import joblib
import pandas as pd
from pathlib import Path

# ── Rutas de los archivos del modelo ─────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
ML_DIR = BASE_DIR / "ml"

# ── Carga del modelo y encoders ──────────────────────────────
model         = joblib.load(ML_DIR / "model.joblib")
le_area       = joblib.load(ML_DIR / "le_area.joblib")
le_crm        = joblib.load(ML_DIR / "le_crm.joblib")
le_crm2       = joblib.load(ML_DIR / "le_crm2.joblib")
le_sex        = joblib.load(ML_DIR / "le_sex.joblib")
le_premis     = joblib.load(ML_DIR / "le_premis.joblib")
le_weapon     = joblib.load(ML_DIR / "le_weapon.joblib")


def prepare_features(data: dict) -> pd.DataFrame:
    """
    Transforma los datos crudos del crimen en el vector de features
    que espera el modelo RandomForest.
    """

    # ── Encoding de variables categoricas ────────────────────
    area_enc    = le_area.transform([data["AREA_NAME"]])[0]
    crm_enc     = le_crm.transform([data["CRM_CD_DESC"]])[0]
    sex_enc     = le_sex.transform([data["VICT_SEX"]])[0]
    premis_enc  = le_premis.transform([data["PREMIS_DESC"]])[0]

    # ── Crimen secundario: si no existe se codifica como 0 ───
    crm2_enc = (
        le_crm2.transform([data["CRM_CD_2_DESC"]])[0]
        if data.get("CRM_CD_2_DESC")
        else 0
    )

    # ── Arma: si no existe se codifica como 0 ────────────────
    weapon_enc = (
        le_weapon.transform([data["WEAPON_DESC"]])[0]
        if data.get("WEAPON_DESC")
        else 0
    )

    # ── Construccion del dataframe de features ────────────────
    features = pd.DataFrame([{
        "AREA_NAME":    area_enc,
        "CRM_CD_DESC":  crm_enc,
        "CRM_CD_2_DESC":crm2_enc,
        "VICT_AGE":     data["VICT_AGE"],
        "VICT_SEX":     sex_enc,
        "PREMIS_DESC":  premis_enc,
        "WEAPON_DESC":  weapon_enc,
        "PART_1_2":     data["PART_1_2"],
        "hour":         data["hour"],
        "month":        data["month"],
        "day_of_week":  data["day_of_week"],
    }])

    return features


def predict(data: dict) -> dict:
    """
    Recibe los datos del crimen, prepara las features,
    aplica el modelo y devuelve la prediccion con probabilidades.
    """

    X = prepare_features(data)

    # ── Prediccion ────────────────────────────────────────────
    clase_idx   = model.predict(X)[0]
    probs       = model.predict_proba(X)[0]

    prob_arrestado     = round(float(probs[1]), 4)
    prob_no_arrestado  = round(float(probs[0]), 4)
    clase_predicha     = "arrestado" if clase_idx == 1 else "no arrestado"
    confianza          = round(float(max(probs)), 4)

    return {
        "clase_predicha":          clase_predicha,
        "probabilidad_arrestado":  prob_arrestado,
        "probabilidad_no_arrestado": prob_no_arrestado,
        "confianza":               confianza,
        "modelo":                  "RandomForestClassifier"
    }
