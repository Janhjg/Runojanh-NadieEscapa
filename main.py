from fastapi import FastAPI
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
from services import get_all_crimes, fetch_crime_by_id

app = FastAPI(
    title="Runojanh - The Dark Chronicles",
    description="API que transforma crimenes urbanos reales en narrativas de novela negra usando ML, HuggingFace y IA Generativa."
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

@app.get("/crimes/{id}", tags=["Dataset"])  # ← sin response_model
def get_crime_by_id_tara(id: int):
    if id <= 0:
        error_422("El ID debe ser un numero positivo")

    crimen = get_crime_by_id(id)

    if crimen is None:
        error_404(f"No se encontro ningun crimen con ID {id}")

    return crimen
 
# ML
 
# ── ML ────────────────────────────────────────────────────────

@app.post("/predict/new", response_model=PredictOutput, tags=["ML"])
def predict_new(data: PredictNewInput):
    try:
        resultado = predict(data.model_dump())
        return resultado
    except ValueError as e:
        error_422(f"Valor no reconocido por el modelo: {str(e)}")
    except FileNotFoundError:
        error_503("El modelo ML no esta disponible. Ejecuta train.py primero")
    except Exception as e:
        error_503(f"El servicio de prediccion no esta disponible: {str(e)}")


@app.get("/predict/{id}", response_model=PredictByIdResponse, tags=["ML"])
def predict_by_id(id: int):

    # ── Validacion del ID ─────────────────────────────────────
    if id <= 0:
        error_422("El ID debe ser un numero positivo")

    # ── Buscar el crimen en el dataset ────────────────────────
    crimen = get_crime_by_id(id)

    if crimen is None:
        error_404(f"No se encontro ningun crimen con ID {id}")

    # ── Verificar que el caso sigue en investigacion ──────────
    status = crimen.get("STATUS_DESC", "")

    if status in ["Adult Arrest", "Juv Arrest"]:
        error_400(f"El caso {id} ya fue resuelto con arresto. No requiere prediccion")

    # ── Preparar los datos para el modelo ─────────────────────
    try:
        from datetime import datetime
        fecha = datetime.strptime(crimen["DATE_OCC"], "%m/%d/%Y %I:%M:%S %p")
        hora_str = str(crimen.get("TIME_OCC", "0000")).zfill(4)

        datos_modelo = {
            "AREA_NAME":     crimen.get("AREA_NAME"),
            "CRM_CD_DESC":   crimen.get("CRM_CD_DESC"),
            "CRM_CD_2_DESC": crimen.get("CRM_CD_2_DESC"),
            "VICT_AGE":      crimen.get("VICT_AGE", 0),
            "VICT_SEX":      crimen.get("VICT_SEX", "X"),
            "PREMIS_DESC":   crimen.get("PREMIS_DESC"),
            "WEAPON_DESC":   crimen.get("WEAPON_DESC"),
            "PART_1_2":      crimen.get("PART_1_2", 2),
            "hour":          int(hora_str[:2]),
            "month":         fecha.month,
            "day_of_week":   fecha.weekday(),
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
        error_503("El modelo ML no esta disponible. Ejecuta train.py primero")
    except Exception as e:
        error_503(f"El servicio de prediccion no esta disponible: {str(e)}")
 
 
# HuggingFace 
 
@app.post("/classify", response_model=ClassifyOutput, tags=["HuggingFace"])
def classify(data: ClassifyInput):
    pass
 
 
# IA Generativa
 
@app.post("/narrate", response_model=NarrateOutput, tags=["IA Generativa"])
def narrate(data: NarrateInput):
    pass
 
 
# Full Case
 
@app.post("/full-case/new", response_model=FullCaseOutput, tags=["Full Case"])
def full_case_new(data: FullCaseNewInput):
    pass
 
 
@app.get("/full-case/{id}", response_model=FullCaseByIdOutput, tags=["Full Case"])
def full_case_by_id(id: int):
    if id <= 0:
        error_422("El ID debe ser un numero positivo")
 