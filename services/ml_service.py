import joblib
import pandas as pd
from pathlib import Path

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder


# ── Rutas de los archivos del modelo ─────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
ML_DIR = BASE_DIR / "models"

# ── Carga del modelo y encoders ──────────────────────────────

pipeline_model:Pipeline = joblib.load(ML_DIR / "crime_data_model.pkl")
encoderLocation:LabelEncoder = joblib.load(ML_DIR / "encoder_Location.joblib")
encoderVictSex = joblib.load(ML_DIR / "encoder_VictSex.joblib")
encoderVictDescent = joblib.load(ML_DIR / "encoder_VictDescent.joblib")


def prepare_features(data: dict) -> pd.DataFrame:
    """
    Transforma los datos crudos del crimen en el vector de features
    que espera el modelo RandomForest.
    se van a preparar como si los recibiera en el mismo estado que CrimeData_Subconjunto_not_invest.csv dado que los encoders se crearon con ese tipo de datos.
    DATE OCC
    TIME OCC
    AREA``(i
    Rpt Dist
    Part 1-2
    Crm Cd``
    Vict Age
    Vict Sex
    Vict Des
    Premis C
    Weapon U
    Status D
    Crm Cd 2
    Crm Cd 3
    Crm Cd 4
    LOCATION
     """

    # ── Encoding de variables categoricas ────────────────────
    try:
        Vict_Sex        = encoderVictSex.transform([data["Vict_Sex"]])[0]
        Vict_Descent    = encoderVictDescent.transform([data["Vict_Descent"]])[0]
        if data["LOCATION"] not in encoderLocation.classes_:
            location=-1
        else:
            location        = encoderLocation.transform([data["LOCATION"]])[0]

        # ── Desglosando fecha ───
        fecha=pd.to_datetime(data["DATE_OCC"], errors="coerce")
        año=fecha.year
        mes=fecha.month
        dia=fecha.day
    except ValueError():
        raise Exception()

    # ── Construccion del dataframe de features ────────────────
    features = pd.DataFrame([{
        "TIME OCC":        data["TIME_OCC"],
        "AREA":            data["AREA"],
        "Rpt Dist No":     data["Rpt_Dist_No"],
        "Part 1-2":        data["Part_1-2"],
        "Crm Cd":          data["Crm_Cd"],
        "Vict Age":        data["Vict_Age"],
        "Vict Sex":        Vict_Sex,
        "Vict Descent":    Vict_Descent,
        "Premis Cd":       data["Premis_Cd"],
        "Weapon Used Cd":  data["Weapon_Used_Cd"],
        "Crm Cd 2":        data["Crm_Cd_2"],
        "Crm Cd 3":        data["Crm_Cd_3"],
        "Crm Cd 4":        data["Crm_Cd_4"],
        "LOCATION":        location,
        "YEAR OCC":        año,
        "MONTH OCC":       mes,
        "DAY OCC":         dia
    }])

    return features


def predict(data: dict):
    """
    Recibe los datos del crimen, prepara las features,
    aplica el modelo y devuelve la prediccion con probabilidades.
    """

    X = prepare_features(data)

    # ── Prediccion ────────────────────────────────────────────
    clase_idx   = pipeline_model.predict(X)
    # probs       = model.predict_proba(X)[0]

    # prob_arrestado     = round(float(probs[1]), 4)
    # prob_no_arrestado  = round(float(probs[0]), 4)
    # clase_predicha     = "arrestado" if clase_idx == 1 else "no arrestado"
    # confianza          = round(float(max(probs)), 4)

    return clase_idx

# {
#         "clase_predicha":          clase_predicha,
#         "probabilidad_arrestado":  prob_arrestado,
#         "probabilidad_no_arrestado": prob_no_arrestado,
#         "confianza":               confianza,
#         "modelo":                  "RandomForestClassifier"
#     }
if __name__=="__main__":
    df=pd.read_csv("data/crimeData_subconjunto_Investigacion.csv")
    df=df.rename(columns={
            "DATE OCC":"DATE_OCC",
            "TIME OCC":"TIME_OCC",
            "AREA":"AREA",
            "Rpt Dist No":"Rpt_Dist_No",
            "Part 1-2":"Part_1-2",
            "Crm Cd":"Crm_Cd",
            "Vict Age":"Vict_Age",
            "Vict Sex":"Vict_Sex",
            "Vict Descent":"Vict_Descent",
            "Premis Cd":"Premis_Cd",
            "Weapon Used Cd":"Weapon_Used_Cd",
            "Crm Cd 2":"Crm_Cd_2",
            "Crm Cd 3":"Crm_Cd_3",
            "Crm Cd 4":"Crm_Cd_4",
            "LOCATION":"LOCATION"
        })
    numcaso=0
    listErrores=list()
    listpredicts=list()
    for s in range(0, 5000,1):
        datacaso = df.iloc[numcaso].to_dict()

        numcaso+=1
        
        
        try:
            cadenaPrediccion =str(predict(datacaso))
            listpredicts.append(cadenaPrediccion)

        except Exception():
            listErrores.append(numcaso)
    seriePredicciones=pd.Series(listpredicts)
    print(f"han habido {len(listErrores)} erroes y {seriePredicciones.value_counts().head()} \n longuitud de predicciones {len(listpredicts)}")
        