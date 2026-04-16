from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Optional
from collections import Counter
 
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
    create_user_case,
    get_all_user_cases,
    fetch_user_case_by_id,
    update_user_case,
    delete_user_case,
    generar_cronica
)
from services import predict
from services import construir_clasificacion
from services.tts_service import generate_voice_narration
from services.pdf_service import generate_case_pdf

class TTSInput(BaseModel):
    text: str

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

# Coordenadas aproximadas de las estaciones centrales de cada área de la LAPD
AREA_COORDINATES = {
    "Central": [34.0443, -118.2474],
    "Southwest": [34.0105, -118.3298],
    "Hollenbeck": [34.0450, -118.2121],
    "Harbor": [33.7577, -118.2882],
    "Hollywood": [34.0958, -118.3307],
    "77th Street": [33.9703, -118.2731],
    "Newton": [34.0124, -118.2565],
    "Pacific": [33.9917, -118.4190],
    "Van Nuys": [34.1867, -118.4481],
    "West LA": [34.0440, -118.4507],
    "Northeast": [34.1192, -118.2494],
    "77th street": [33.9703, -118.2731],
    "Mission": [34.2727, -118.4682],
    "Topanga": [34.2214, -118.6019],
    "Olympic": [34.0502, -118.2915],
    "West Valley": [34.1934, -118.5361],
    "Southeast": [33.9377, -118.2759],
    "North Hollywood": [34.1718, -118.3842],
    "Foothill": [34.2533, -118.4104],
    "Devonshire": [34.2570, -118.5276],
    "Rampart": [34.0567, -118.2671],
    "Wilshire": [34.0467, -118.3424],
}
 
 
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
    area_name: Optional[str] = None,
    crime_desc: Optional[str] = None,
    vict_age_min: Optional[int] = None,
    vict_age_max: Optional[int] = None,
    time_occ_min: Optional[int] = None,
    time_occ_max: Optional[int] = None,
    status_desc: Optional[str] = None,
    weapon_desc: Optional[str] = None,
    premis_desc: Optional[str] = None,
    dr_no: Optional[int] = None,
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
        area_name=area_name,
        crime_desc=crime_desc,
        vict_age_min=vict_age_min,
        vict_age_max=vict_age_max,
        time_occ_min=time_occ_min,
        time_occ_max=time_occ_max,
        status_desc=status_desc,
        weapon_desc=weapon_desc,
        premis_desc=premis_desc,
        dr_no=dr_no
    )

@app.get("/crimes/meta", tags=["Dataset"])
def crimes_meta():
    from services.dataset_services import get_unique_values
    
    unique_areas = get_unique_values("AREA_NAME")
    unique_descents = get_unique_values("Vict_Descent")
    unique_sexes = get_unique_values("Vict_Sex")
    unique_statuses = get_unique_values("Status_Desc")
    unique_weapons = get_unique_values("Weapon_Desc")
    unique_crimes = get_unique_values("Crm_Cd_Desc")

    descents_map = {
        "A": "Asiático", "B": "Negro", "C": "Chino", "D": "Camboyano",
        "F": "Filipino", "G": "Guameño", "H": "Hispano", "I": "Indígena",
        "J": "Japonés", "K": "Coreano", "O": "Otros", "P": "Isleño",
        "S": "Samoano", "U": "Hawaiano", "V": "Vietnamita", "W": "Blanco",
        "X": "Desconocido", "Z": "India"
    }

    return {
        "areas": [{"id": i, "name": a} for i, a in enumerate(unique_areas)],
        "descents": [{"code": c, "label": descents_map.get(c, c)} for c in unique_descents],
        "sexes": [{"code": s, "label": "Masculino" if s == "M" else "Femenino" if s == "F" else "Otros"} for s in unique_sexes],
        "statuses": unique_statuses,
        "weapons": unique_weapons,
        "crimes": unique_crimes
    }

@app.get("/user-cases", tags=["Dataset"])
def user_cases_list(
    limit: int = 20,
    offset: int = 0,
):
    if limit <= 0 or offset < 0:
        error_422("limit debe ser mayor que 0 y offset no puede ser negativo")
    return get_all_user_cases(limit, offset)


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
        resultado = predict(datos)
        nuevo_caso = create_user_case(datos)
        update_user_case(nuevo_caso["user_case_id"], {"prediccion": resultado})
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
        crimen = fetch_user_case_by_id(id)

    if crimen is None:
        error_404(f"No se encontro ningun crimen ni caso de usuario con ID {id}")

    # Permítelo aunque esté cerrado: queremos predecir retrospectivamente
    try:
        # El crimen del dataset tiene columnas con _ por el rename
        # Casos de usuario las tienen con espacios por Pydantic
        datos_modelo = {
            "DATE OCC":      crimen.get("DATE_OCC", crimen.get("DATE OCC", "")),
            "TIME OCC":      crimen.get("TIME_OCC", crimen.get("TIME OCC", 0)),
            "AREA NAME":     crimen.get("AREA_NAME", crimen.get("AREA NAME", "")),
            "Rpt Dist No":   crimen.get("Rpt_Dist_No", crimen.get("Rpt Dist No", 0)),
            "Part 1-2":      crimen.get("Part_1_2", crimen.get("Part 1-2", 2)),
            "Crm Cd Desc":   crimen.get("Crm_Cd_Desc", crimen.get("Crm Cd Desc", "")),
            "Vict Age":      crimen.get("Vict_Age", crimen.get("Vict Age", 0)),
            "Vict Sex":      crimen.get("Vict_Sex", crimen.get("Vict Sex", "X")),
            "Vict Descent":  crimen.get("Vict_Descent", crimen.get("Vict Descent", "X")),
            "Premis Desc":   crimen.get("Premis_Desc", crimen.get("Premis Desc", "")),
            "Weapon Desc":   crimen.get("Weapon_Desc", crimen.get("Weapon Desc", None)),
            "Crm Cd 2 Desc": crimen.get("Crm_Cd_2_Desc", crimen.get("Crm Cd 2 Desc", None)),
            "Crm Cd 3 Desc": crimen.get("Crm_Cd_3_Desc", crimen.get("Crm Cd 3 Desc", None)),
            "Crm Cd 4 Desc": crimen.get("Crm_Cd_4_Desc", crimen.get("Crm Cd 4 Desc", None)),
        }

        resultado = predict(datos_modelo)
        
        # Guardar si es caso de usuario
        if not fetch_crime_by_id(id):  
            update_user_case(id, {"prediccion": resultado})

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

@app.get("/classify/{id}", tags=["HuggingFace"])
def classify_by_id(id: int):
    crimen_db = fetch_crime_by_id(id)
    if not crimen_db:
        crimen_db = fetch_user_case_by_id(id)
    if not crimen_db:
        raise HTTPException(status_code=404, detail=f"Caso {id} no encontrado")
    
    # Normalización de datos para los servicios
    datos_modelo = {
        "DATE OCC":      crimen_db.get("DATE_OCC", crimen_db.get("DATE OCC", "")),
        "TIME OCC":      crimen_db.get("TIME_OCC", crimen_db.get("TIME OCC", 0)),
        "AREA NAME":     crimen_db.get("AREA_NAME", crimen_db.get("AREA NAME", "")),
        "Rpt Dist No":   crimen_db.get("Rpt_Dist_No", crimen_db.get("Rpt Dist No", 0)),
        "Part 1-2":      crimen_db.get("Part_1_2", crimen_db.get("Part 1-2", 2)),
        "Crm Cd Desc":   crimen_db.get("Crm_Cd_Desc", crimen_db.get("Crm Cd Desc", "")),
        "Vict Age":      crimen_db.get("Vict_Age", crimen_db.get("Vict Age", 0)),
        "Vict Sex":      crimen_db.get("Vict_Sex", crimen_db.get("Vict Sex", "X")),
        "Vict Descent":  crimen_db.get("Vict_Descent", crimen_db.get("Vict Descent", "X")),
        "Premis Desc":   crimen_db.get("Premis_Desc", crimen_db.get("Premis Desc", "")),
        "Weapon Desc":   crimen_db.get("Weapon_Desc", crimen_db.get("Weapon Desc", None)),
        "Crm Cd 2 Desc": crimen_db.get("Crm_Cd_2_Desc", crimen_db.get("Crm Cd 2 Desc", None)),
        "Crm Cd 3 Desc": crimen_db.get("Crm_Cd_3_Desc", crimen_db.get("Crm Cd 3 Desc", None)),
        "Crm Cd 4 Desc": crimen_db.get("Crm_Cd_4_Desc", crimen_db.get("Crm Cd 4 Desc", None)),
    }
    try:
        pred_res = predict(datos_modelo)
    except Exception as e:
        pred_res = {"clase_predicha": "desconocido", "confianza": 0}
        
    try:
        clasificacion = construir_clasificacion(datos_modelo, VObjetiva=pred_res.get("clase_predicha"))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    clasificacion_obj = {
        "clasificacion_hf": clasificacion,
        "texto_construido": clasificacion["texto_construido"],
        "todas_etiquetas": clasificacion["todas_etiquetas"]
    }

    if not fetch_crime_by_id(id):
        update_user_case(id, {"clasificacion": clasificacion_obj})

    return {
        "registro_id": id,
        **clasificacion_obj
    }
 
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

@app.get("/narrate/{id}", tags=["IA Generativa"])
def narrate_by_id(id: int):
    crimen_db = fetch_crime_by_id(id)
    if not crimen_db:
        crimen_db = fetch_user_case_by_id(id)
    if not crimen_db:
        raise HTTPException(status_code=404, detail=f"Caso {id} no encontrado")
        
    # Normalización de datos para los servicios
    datos_modelo = {
        "DATE OCC":      crimen_db.get("DATE_OCC", crimen_db.get("DATE OCC", "")),
        "TIME OCC":      crimen_db.get("TIME_OCC", crimen_db.get("TIME OCC", 0)),
        "AREA NAME":     crimen_db.get("AREA_NAME", crimen_db.get("AREA NAME", "")),
        "Rpt Dist No":   crimen_db.get("Rpt_Dist_No", crimen_db.get("Rpt Dist No", 0)),
        "Part 1-2":      crimen_db.get("Part_1_2", crimen_db.get("Part 1-2", 2)),
        "Crm Cd Desc":   crimen_db.get("Crm_Cd_Desc", crimen_db.get("Crm Cd Desc", "")),
        "Vict Age":      crimen_db.get("Vict_Age", crimen_db.get("Vict Age", 0)),
        "Vict Sex":      crimen_db.get("Vict_Sex", crimen_db.get("Vict Sex", "X")),
        "Vict Descent":  crimen_db.get("Vict_Descent", crimen_db.get("Vict Descent", "X")),
        "Premis Desc":   crimen_db.get("Premis_Desc", crimen_db.get("Premis Desc", "")),
        "Weapon Desc":   crimen_db.get("Weapon_Desc", crimen_db.get("Weapon Desc", None)),
        "Crm Cd 2 Desc": crimen_db.get("Crm_Cd_2_Desc", crimen_db.get("Crm Cd 2 Desc", None)),
        "Crm Cd 3 Desc": crimen_db.get("Crm_Cd_3_Desc", crimen_db.get("Crm Cd 3 Desc", None)),
        "Crm Cd 4 Desc": crimen_db.get("Crm_Cd_4_Desc", crimen_db.get("Crm Cd 4 Desc", None)),
    }
    try:
        pred_res = predict(datos_modelo)
        clasificacion = construir_clasificacion(datos_modelo, VObjetiva=pred_res.get("clase_predicha"))
        cronica = generar_cronica(datos_modelo, pred_res, clasificacion["todas_etiquetas"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    if not fetch_crime_by_id(id):
        update_user_case(id, {"cronica": cronica})
        
    return {
        "registro_id": id,
        "cronica": cronica
    }

@app.post("/tts/narrate", tags=["IA Generativa"])
def tts_narrate(data: TTSInput):
    try:
        audio_content = generate_voice_narration(data.text)
        return Response(content=audio_content, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 
 
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
        
        # Guardar todo en memoria
        nuevo_caso = create_user_case(datos_dict)
        update_user_case(nuevo_caso["user_case_id"], {
            "prediccion": prediccion,
            "clasificacion": {
                "clasificacion_hf": clasificacion,
                "texto_construido": clasificacion["texto_construido"],
                "todas_etiquetas": clasificacion["todas_etiquetas"]
            },
            "cronica": cronica
        })
        
        return FullCaseOutput(
            id               = nuevo_caso["user_case_id"],
            datos_caso       = data.datos_crimen,
            prediccion_ml    = prediccion,
            clasificacion_hf = clasificacion,
            cronica          = cronica
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en proceso Full Case: {str(e)}")


@app.get("/full-case/{id}", response_model=FullCaseByIdOutput, tags=["Full Case"])
def full_case_by_id(id: int):
    """
    Simula el proceso completo "Full Case" para un ID:
    1. Predicción (Random Forest)
    2. Clasificación de estilos e intenciones (BART-Large)
    3. Crónica literaria (Gemma)
    """
    try:
        if id <= 0:
            error_422("El ID debe ser un numero positivo")

        crimen = fetch_crime_by_id(id)
        if crimen is None:
            crimen = fetch_user_case_by_id(id)
        if crimen is None:
            error_404(f"No se encontro ningun crimen ni caso de usuario con ID {id}")

        # Normalización de datos para los servicios
        def to_int(v, default=0):
            if isinstance(v, int): return v
            if isinstance(v, str):
                if "Grave" in v or "1" in v: return 1
                if "Leve" in v or "2" in v: return 2
                try: return int(float(v))
                except: pass
            return default

        datos_modelo = {
            "DATE OCC":      crimen.get("DATE_OCC", crimen.get("DATE OCC", "")),
            "TIME OCC":      to_int(crimen.get("TIME_OCC", crimen.get("TIME OCC", 1200))),
            "AREA NAME":     crimen.get("AREA_NAME", crimen.get("AREA NAME", "")),
            "Rpt Dist No":   to_int(crimen.get("Rpt_Dist_No", crimen.get("Rpt Dist No", 0))),
            "Part 1-2":      to_int(crimen.get("Part_1_2", crimen.get("Part 1-2", 1)), default=1),
            "Crm Cd Desc":   crimen.get("Crm_Cd_Desc", crimen.get("Crm Cd Desc", "")),
            "Vict Age":      to_int(crimen.get("Vict_Age", crimen.get("Vict Age", 0))),
            "Vict Sex":      crimen.get("Vict_Sex", crimen.get("Vict Sex", "X")),
            "Vict Descent":  crimen.get("Vict_Descent", crimen.get("Vict Descent", "X")),
            "Premis Desc":   crimen.get("Premis_Desc", crimen.get("Premis Desc", "")),
            "Weapon Desc":   crimen.get("Weapon_Desc", crimen.get("Weapon Desc", None)),
            "Crm Cd 2 Desc": crimen.get("Crm_Cd_2_Desc", crimen.get("Crm Cd 2 Desc", None)),
            "Crm Cd 3 Desc": crimen.get("Crm_Cd_3_Desc", crimen.get("Crm Cd 3 Desc", None)),
            "Crm Cd 4 Desc": crimen.get("Crm_Cd_4_Desc", crimen.get("Crm Cd 4 Desc", None)),
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

        if not fetch_crime_by_id(id):
             update_user_case(id, {
                 "prediccion": prediccion,
                 "clasificacion": {
                     "clasificacion_hf": clasificacion,
                     "texto_construido": clasificacion["texto_construido"],
                     "todas_etiquetas": clasificacion["todas_etiquetas"]
                 },
                 "cronica": cronica
             })

        return FullCaseByIdOutput(
            id               = id,
            datos_caso       = crimen,
            prediccion_ml    = prediccion,
            clasificacion_hf = clasificacion,
            cronica          = cronica
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en proceso Full Case por ID: {str(e)}")

@app.get("/export/pdf/{id}", tags=["IA Generativa"])
def export_case_pdf(id: int):
    try:
        # Reutilizamos la lógica de Full Case para asegurar que tenemos todos los datos
        crimen_db = fetch_crime_by_id(id)
        if not crimen_db:
            crimen_db = fetch_user_case_by_id(id)
        if not crimen_db:
            raise HTTPException(status_code=404, detail=f"Caso {id} no encontrado")
            
        # Normalización y obtención de datos completos (ML + NLP + GenAI)
        datos_modelo = {
            "DATE OCC":      crimen_db.get("DATE_OCC", crimen_db.get("DATE OCC", "")),
            "TIME OCC":      crimen_db.get("TIME_OCC", crimen_db.get("TIME OCC", 0)),
            "AREA NAME":     crimen_db.get("AREA_NAME", crimen_db.get("AREA NAME", "")),
            "Rpt Dist No":   crimen_db.get("Rpt_Dist_No", crimen_db.get("Rpt Dist No", 0)),
            "Part 1-2":      crimen_db.get("Part_1_2", crimen_db.get("Part 1-2", 2)),
            "Crm Cd Desc":   crimen_db.get("Crm_Cd_Desc", crimen_db.get("Crm Cd Desc", "")),
            "Vict Age":      crimen_db.get("Vict_Age", crimen_db.get("Vict Age", 0)),
            "Vict Sex":      crimen_db.get("Vict_Sex", crimen_db.get("Vict Sex", "X")),
            "Vict Descent":  crimen_db.get("Vict_Descent", crimen_db.get("Vict Descent", "X")),
            "Premis Desc":   crimen_db.get("Premis_Desc", crimen_db.get("Premis Desc", "")),
            "Weapon Desc":   crimen_db.get("Weapon_Desc", crimen_db.get("Weapon Desc", None)),
        }
        
        # Generar componentes si no existen (simulado para el PDF)
        pred_res = predict(datos_modelo)
        clasificacion = construir_clasificacion(datos_modelo, VObjetiva=pred_res.get("clase_predicha"))
        cronica = generar_cronica(datos_modelo, pred_res, clasificacion["todas_etiquetas"])
        
        pdf_data = {
            "id": id,
            **datos_modelo,
            "prediccion": pred_res,
            "cronica": cronica
        }
        
        pdf_content = generate_case_pdf(pdf_data)
        
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=Expediente_LAPD_{id}.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando PDF: {str(e)}")

@app.get("/stats/summary", tags=["Estadísticas"])
def get_stats_summary(
    area_name: Optional[str] = None,
    crime_desc: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    vict_age_min: Optional[int] = None,
    vict_age_max: Optional[int] = None,
    time_occ_min: Optional[int] = None,
    time_occ_max: Optional[int] = None,
    vict_sex: Optional[str] = None,
    vict_descent: Optional[str] = None,
    status_desc: Optional[str] = None,
    weapon_desc: Optional[str] = None,
    premis_desc: Optional[str] = None,
    dr_no: Optional[int] = None,
):
    from services.dataset_services import get_filtered_df
    filtered = get_filtered_df(
        area_name=area_name,
        crime_desc=crime_desc,
        date_from=date_from,
        date_to=date_to,
        vict_age_min=vict_age_min,
        vict_age_max=vict_age_max,
        time_occ_min=time_occ_min,
        time_occ_max=time_occ_max,
        vict_sex=vict_sex,
        vict_descent=vict_descent,
        status_desc=status_desc,
        weapon_desc=weapon_desc,
        premis_desc=premis_desc,
        dr_no=dr_no
    )
    
    if filtered.empty:
        return {
            "total_casos": 0,
            "arrestos": 0,
            "pendientes": 0,
            "tasa_arresto": 0,
            "top_crimenes": {},
            "distribucion_horaria": {}
        }
    
    total = len(filtered)
    
    # Categorías de Estatus
    arrested = len(filtered[filtered["Status_Desc"].str.contains("Arrest", case=False, na=False)])
    no_arrested = len(filtered[filtered["Status_Desc"].str.contains("Other", case=False, na=False)])
    invest = len(filtered[filtered["Status_Desc"].str.contains("Invest Cont", case=False, na=False)])
    
    pending = total - arrested
    
    # Top Crímenes
    top_crimes = filtered["Crm_Cd_Desc"].value_counts().head(5).to_dict()
    
    # Crimen por hora (distribución)
    filtered_stats = filtered.copy()
    filtered_stats["hour"] = (filtered_stats["TIME_OCC"] // 100).astype(int)
    hourly_dist = filtered_stats["hour"].value_counts().sort_index().to_dict()
    
    return {
        "total_casos": total,
        "arrestos": arrested,
        "no_arrestos": no_arrested,
        "en_investigacion": invest,
        "tasa_arresto": round((arrested / total) * 100, 2) if total > 0 else 0,
        "top_crimenes": top_crimes,
        "distribucion_horaria": hourly_dist
    }

@app.get("/stats/geo", tags=["Estadísticas"])
def get_stats_geo(
    area_name: Optional[str] = None,
    crime_desc: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    vict_age_min: Optional[int] = None,
    vict_age_max: Optional[int] = None,
    time_occ_min: Optional[int] = None,
    time_occ_max: Optional[int] = None,
    vict_sex: Optional[str] = None,
    vict_descent: Optional[str] = None,
    status_desc: Optional[str] = None,
    weapon_desc: Optional[str] = None,
    premis_desc: Optional[str] = None,
    dr_no: Optional[int] = None,
):
    from services.dataset_services import get_filtered_df
    filtered = get_filtered_df(
        area_name=area_name,
        crime_desc=crime_desc,
        date_from=date_from,
        date_to=date_to,
        vict_age_min=vict_age_min,
        vict_age_max=vict_age_max,
        time_occ_min=time_occ_min,
        time_occ_max=time_occ_max,
        vict_sex=vict_sex,
        vict_descent=vict_descent,
        status_desc=status_desc,
        weapon_desc=weapon_desc,
        premis_desc=premis_desc,
        dr_no=dr_no
    )
    
    if filtered.empty:
        return []
    
    # Tomamos una muestra para no saturar el mapa si hay demasiados (ej. los últimos 300)
    sample_size = min(300, len(filtered))
    df_sample = filtered.tail(sample_size).copy()
    
    geo_data = []
    coords_lower = {k.lower(): v for k, v in AREA_COORDINATES.items()}
    
    import random

    for _, row in df_sample.iterrows():
        area = str(row["AREA_NAME"]).strip().lower()
        if area in coords_lower:
            base_lat, base_lon = coords_lower[area]
            
            # Aplicar Jitter (desplazamiento aleatorio ligero)
            jitter_lat = base_lat + (random.uniform(-0.015, 0.015))
            jitter_lon = base_lon + (random.uniform(-0.015, 0.015))
            
            # Determinar estatus para el color
            status_desc = str(row["Status_Desc"]).lower()
            if "arrest" in status_desc:
                cat = "arrest"
            elif "other" in status_desc:
                cat = "no_arrest"
            else:
                cat = "investigation"
                
            geo_data.append({
                "id": str(row["DR_NO"]),
                "crime": str(row["Crm_Cd_Desc"]),
                "area": row["AREA_NAME"],
                "lat": jitter_lat,
                "lon": jitter_lon,
                "status": cat
            })
            
    return geo_data
 