from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Optional
 
from schemas import (
    CrimeListResponse, CrimeDetailResponse,
    PredictNewInput, PredictOutput, PredictByIdResponse,
    ClassifyInput, ClassifyOutput,
    NarrateInput, NarrateOutput,
    FullCaseNewInput, FullCaseOutput, FullCaseByIdOutput
)
from services import error_400, error_404, error_422, error_503, error_504
from services import (
    get_all_crimes,
    fetch_crime_by_id,
    create_user_case,      # ← falta este
    get_all_user_cases,
    fetch_user_case_by_id,
    delete_user_case,
    generar_cronica
)
from services import predict
from services import construir_clasificacion

app = FastAPI(
    title="Runojanh - The Dark Chronicles",
    description="API que transforma crimenes urbanos reales en narrativas de novela negra usando ML, HuggingFace y IA Generativa."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
 
@app.get("/", tags=["Home"])
def home():
    return {
        "nombre": "Runojanh - NadieEscapa",
        "descripcion": (
            "API que analiza crimenes urbanos reales del dataset de Los Angeles. "
            "Predice si un caso sera resuelto con arresto usando Machine Learning, "
            "clasifica el crimen con una etiqueta narrativa sentimental usando HuggingFace "
            "y genera una cronica de novela negra usando IA Generativa."
        ),
        "tecnologias": {
            "ml": "Tururiru",
            "huggingface": "facebook/bart-large-mnli (zero-shot-classification)",
            "ia_generativa": "Gemini 2.0 Flash (Google)",
            "dataset": "Los Angeles Crime Data 2020-2023"
        },
        "endpoints": {
            "home": "GET /",
            "status": "GET /status",
            "crimes": "GET /crimes",
            "crime_by_id": "GET /crimes/{id}",
            "predict_new": "POST /predict/new",
            "predict_by_id": "GET /predict/{id}",
            "classify": "POST /classify",
            "narrate": "POST /narrate",
            "full_case_new": "POST /full-case/new",
            "full_case_by_id": "GET /full-case/{id}"
        },
        "documentacion": "http://localhost:8000/docs"
    }
 
@app.get("/status", tags=["Home"])
def status():
    return {
        "status": "ok",
        "mensaje": "API operativa",
        "servicios": {
            "api": "ok"
        }
    }
    
# Dataset

# ── Dataset ───────────────────────────────────────────────────

@app.get("/crimes", tags=["Dataset"])
def crimes_list(
    limit: int = 20,
    offset: int = 0,
    area: Optional[int] = None,
    crm_cd: Optional[int] = None,
    part_1_2: Optional[int] = None,
    vict_sex: Optional[str] = None,
    vict_descent: Optional[str] = None,
    premis_cd: Optional[int] = None,
    weapon_used_cd: Optional[int] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
):
    if limit <= 0 or offset < 0:
        error_422("limit debe ser mayor que 0 y offset no puede ser negativo")
 
    return get_all_crimes(
        limit=limit,
        offset=offset,
        area=area,
        crm_cd=crm_cd,
        part_1_2=part_1_2,
        vict_sex=vict_sex,
        vict_descent=vict_descent,
        premis_cd=premis_cd,
        weapon_used_cd=weapon_used_cd,
        date_from=date_from,
        date_to=date_to,
    )

@app.get("/crimes/{id}", tags=["Dataset"])
def get_crime_by_id(id: int):
    if id <= 0:
        error_422("El ID debe ser un numero positivo")

    crimen = fetch_crime_by_id(id)

    if crimen is None:
        error_404(f"No se encontro ningun crimen con ID {id}")

    return crimen
 
# ML
 
# ── ML ────────────────────────────────────────────────────────

@app.post("/predict/new", response_model=PredictOutput, tags=["ML"])
def predict_new(data: PredictNewInput):
    try:
        datos = data.model_dump(by_alias=True)
        print("DATOS QUE LLEGAN AL MODELO:", datos)  # ← añade esto
        resultado = predict(datos)
        create_user_case(datos)
        return resultado
    except ValueError as e:
        error_422(f"Valor no reconocido por el modelo: {str(e)}")
    except FileNotFoundError:
        error_503("El modelo ML no esta disponible")
    except Exception as e:
        error_503(f"Servicio de prediccion no disponible: {str(e)}")

@app.get("/predict/{id}", response_model=PredictByIdResponse, tags=["ML"])
def predict_by_id(id: int):
    if id <= 0:
        error_422("El ID debe ser un numero positivo")

    crimen = fetch_crime_by_id(id)

    if crimen is None:
        error_404(f"No se encontro ningun crimen con ID {id}")

    status = crimen.get("Status_Desc", "")

    if status in ["Adult Arrest", "Juv Arrest"]:
        error_400(f"El caso {id} ya fue resuelto con arresto")

    if status in ["Adult Other", "Juv Other"]:
        error_400(f"El caso {id} ya fue cerrado sin arresto")

    try:
        # El crimen del dataset tiene columnas con _ por el rename
        # Hay que devolverlas a los nombres originales con espacio
        # que es lo que espera ml_service.prepare_features()
        datos_modelo = {
            "DATE OCC":      crimen.get("DATE_OCC", ""),
            "TIME OCC":      crimen.get("TIME_OCC", 0),
            "AREA NAME":     crimen.get("AREA_NAME", ""),
            "Rpt Dist No":   crimen.get("Rpt_Dist_No", 0),
            "Part 1-2":      crimen.get("Part_1_2", 2),
            "Crm Cd Desc":   crimen.get("Crm_Cd_Desc", ""),
            "Vict Age":      crimen.get("Vict_Age", 0),
            "Vict Sex":      crimen.get("Vict_Sex", "X"),
            "Vict Descent":  crimen.get("Vict_Descent", ""),
            "Premis Desc":   crimen.get("Premis_Desc", ""),
            "Weapon Desc":   crimen.get("Weapon_Desc", None),
            "Crm Cd 2 Desc": None,
            "Crm Cd 3 Desc": None,
            "Crm Cd 4 Desc": None,
        }

        resultado = predict(datos_modelo)

        return {
            "id": id,
            "datos_caso": crimen,
            "prediccion": resultado
        }

    except ValueError as e:
        error_422(f"Valor no reconocido por el modelo: {str(e)}")
    except FileNotFoundError:
        error_503("El modelo ML no esta disponible")
    except Exception as e:
        error_503(f"Servicio de prediccion no disponible: {str(e)}")
 
# HuggingFace 
@app.post("/classify", response_model=ClassifyOutput, tags=["HuggingFace"])
def classify(data: ClassifyInput):
    try:
        datos_dict = data.datos_crimen.model_dump(by_alias=True)  # ✅ el service ya hace el remap
        resultado  = construir_clasificacion(datos_dict, VObjetiva=data.prediccion_ml.clase_predicha)

        return ClassifyOutput(
            etiqueta         = resultado["etiqueta"],
            confianza        = resultado["confianza"],
            texto_construido = resultado["texto_construido"],
            todas_etiquetas  = resultado["todas_etiquetas"],
            modelo           = resultado["modelo"],
        )

    except KeyError as e:
        raise HTTPException(status_code=422, detail=f"Campo faltante en datos del crimen: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en clasificación HuggingFace: {str(e)}")
 
# IA Generativa
 
@app.post("/narrate", response_model=NarrateOutput, tags=["IA Generativa"])
def narrate(data: NarrateInput):
    try:
        datos_dict = data.datos_crimen.model_dump(by_alias=True)
        pred_dict  = data.prediccion_ml.model_dump()
        
        cronica = generar_cronica(
            datos_crimen = datos_dict,
            prediccion   = pred_dict,
            etiquetas    = data.etiquetas_huggingface
        )

        return NarrateOutput(
            cronica              = cronica,
            palabras             = len(cronica.split()),
            etiquetas_usadas     = data.etiquetas_huggingface,
            clase_predicha_usada = data.prediccion_ml.clase_predicha,
            modelo               = "gemma4:e2b (Ollama)"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en generación narrativa: {str(e)}")
 
 
# Full Case
 
@app.post("/full-case/new", response_model=FullCaseOutput, tags=["Full Case"])
def full_case_new(data: FullCaseNewInput):
    try:
        # 1. ML Prediction
        datos_dict = data.datos_crimen.model_dump(by_alias=True)
        prediccion = predict(datos_dict)
        
        # 2. HuggingFace Classification
        clasificacion = construir_clasificacion(datos_dict, VObjetiva=prediccion["clase_predicha"])
        
        # 3. Generative Narrative (Ollama)
        cronica = generar_cronica(
            datos_crimen = datos_dict,
            prediccion   = prediccion,
            etiquetas    = clasificacion["todas_etiquetas"]
        )
        
        return FullCaseOutput(
            datos_caso       = data.datos_crimen,
            prediccion_ml    = prediccion,
            clasificacion_hf = clasificacion,
            cronica          = cronica
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en proceso Full Case: {str(e)}")


@app.get("/full-case/{id}", response_model=FullCaseByIdOutput, tags=["Full Case"])
def full_case_by_id(id: int):
    if id <= 0:
        error_422("El ID debe ser un numero positivo")

    crimen = fetch_crime_by_id(id)
    if crimen is None:
        error_404(f"No se encontro ningun crimen con ID {id}")

    try:
        # Normalización de datos para los servicios
        datos_modelo = {
            "DATE OCC":      crimen.get("DATE_OCC", ""),
            "TIME OCC":      crimen.get("TIME_OCC", 0),
            "AREA NAME":     crimen.get("AREA_NAME", ""),
            "Rpt Dist No":   crimen.get("Rpt_Dist_No", 0),
            "Part 1-2":      crimen.get("Part_1_2", 2),
            "Crm Cd Desc":   crimen.get("Crm_Cd_Desc", ""),
            "Vict Age":      crimen.get("Vict_Age", 0),
            "Vict Sex":      crimen.get("Vict_Sex", "X"),
            "Vict Descent":  crimen.get("Vict_Descent", ""),
            "Premis Desc":   crimen.get("Premis_Desc", ""),
            "Weapon Desc":   crimen.get("Weapon_Desc", None),
            "Crm Cd 2 Desc": None,
            "Crm Cd 3 Desc": None,
            "Crm Cd 4 Desc": None,
        }

        # 1. ML Prediction
        prediccion = predict(datos_modelo)
        
        # 2. HuggingFace Classification
        clasificacion = construir_clasificacion(datos_modelo, VObjetiva=prediccion["clase_predicha"])
        
        # 3. Generative Narrative (Ollama)
        cronica = generar_cronica(
            datos_crimen = datos_modelo,
            prediccion   = prediccion,
            etiquetas    = clasificacion["todas_etiquetas"]
        )

        return FullCaseByIdOutput(
            id               = id,
            datos_caso       = crimen,
            prediccion_ml    = prediccion,
            clasificacion_hf = clasificacion,
            cronica          = cronica
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en proceso Full Case por ID: {str(e)}")
 