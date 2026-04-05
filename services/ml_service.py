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
mapper_area=pd.read_csv("..\\models\\mapper_area.csv")
mapper_crm=pd.read_csv("..\\models\\mapper_crm.csv")
mapper_premis=pd.read_csv("..\\models\\mapper_premis.csv")
mapper_weapon=pd.read_csv("..\\models\\mapper_weapon.csv")


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

    # Encoding de variables categoricas
  
    if data["Vict_Sex"] not in encoderVictSex.classes_:
        Vict_Sex=-1
    else:
        Vict_Sex = encoderVictSex.transform([data["Vict_Sex"]])[0]
    
    if data["Vict_Descent"] not in encoderVictDescent.classes_:
        Vict_Descent=-1
    else:
        Vict_Descent = encoderVictDescent.transform([data["Vict_Descent"]])[0]

    if data["LOCATION"] not in encoderLocation.classes_:
        location=-1
    else:
        location = encoderLocation.transform([data["LOCATION"]])[0]

    # Desglosando fecha
    fecha=pd.to_datetime(data["DATE_OCC"], errors="coerce")
    año=fecha.year
    mes=fecha.month
    dia=fecha.day
    
    #mapeando categoricas.
    #AREA
    if data["AREA NAME"]==None or data["AREA NAME"] not in mapper_area["AREA NAME"]:
        areaCode=0
    else:
        areaCode=int(mapper_area[mapper_area["AREA NAME"]==data["AREA NAME"]]["AREA"].iloc(0))

    #crimenes
    if data["Crm Cd Desc"]==None or data["Crm Cd Desc"] not in mapper_crm["Crm Cd Desc"]:
        Crm1Code=0
    else:
        Crm1Code=int(mapper_crm[mapper_crm["Crm Cd Desc"]==data["Crm Cd Desc"]]["Crm Cd"].iloc(0))

    #crimenes 2
    if data["Crm Cd Desc 2"]==None or data["Crm Cd Desc 2"] not in mapper_crm["Crm Cd Desc"]:
        Crm2Code=0
    else:
        Crm2Code=int(mapper_crm[mapper_crm["Crm Cd Desc"]==data["Crm Cd Desc 2"]]["Crm Cd"].iloc(0))

    #crimenes 3
    if data["Crm Cd Desc 3"]==None or data["Crm Cd Desc 3"] not in mapper_crm["Crm Cd Desc"]:
        Crm3Code=0
    else:
        Crm3Code=int(mapper_crm[mapper_crm["Crm Cd Desc"]==data["Crm Cd Desc 3"]]["Crm Cd"].iloc(0))

     #crimenes 4
    if data["Crm Cd Desc 4"]==None or data["Crm Cd Desc 4"] not in mapper_crm["Crm Cd Desc"]:
        Crm4Code=0
    else:
        Crm4Code=int(mapper_crm[mapper_crm["Crm Cd Desc"]==data["Crm Cd Desc 4"]]["Crm Cd"].iloc(0))

    #Premis Cd
    if data["Premis Desc"]==None or data["Premis Desc"] not in mapper_premis["Premis Desc"]:
        premisCode=0
    else:
        premisCode=int(mapper_premis[mapper_premis["Premis Desc"]==data["Premis Desc"]]["Premis Cd"].iloc(0))

    #Weapon Used Cd
    if data["Weapon Desc"]==None or data["Weapon Desc"] not in mapper_weapon["Weapon Desc"]:
        weaponCode=0
    else:
        weaponCode=int(mapper_weapon[mapper_weapon["Weapon Desc"]==data["Weapon Desc"]]["Weapon Used Cd"].iloc(0))
    
       

    # Construccion del dataframe de features
    features = pd.DataFrame([{
        "TIME OCC":        data["TIME_OCC"],
        "AREA":           areaCode,
        "Rpt Dist No":     data["Rpt_Dist_No"],
        "Part 1-2":        data["Part_1-2"],
        "Crm Cd":          Crm1Code,
        "Vict Age":        data["Vict_Age"],
        "Vict Sex":        Vict_Sex,
        "Vict Descent":    Vict_Descent,
        "Premis Cd":       premisCode,
        "Weapon Used Cd":  weaponCode,
        "Crm Cd 2":        Crm2Code,
        "Crm Cd 3":        Crm3Code,
        "Crm Cd 4":        Crm4Code,
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
        