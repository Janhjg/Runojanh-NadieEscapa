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
    create_user_case,
    get_all_user_cases,
    fetch_user_case_by_id,
    update_user_case,
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

@app.get("/crimes/meta", tags=["Dataset"])
def crimes_meta():
    """Devuelve los valores únicos disponibles para los filtros desplegables del explorador."""
    from services.dataset_services import df
    if df.empty:
        return {}
    
    areas_raw = df[["AREA", "AREA_NAME"]].drop_duplicates().sort_values("AREA_NAME")
    areas = [{"id": int(r["AREA"]), "name": str(r["AREA_NAME"])} for _, r in areas_raw.iterrows()]
    
    descents_map = {
        "A": "Asiática", "B": "Negra", "C": "China", "D": "Camboyana",
        "F": "Filipina", "G": "Guameña", "H": "Hispana/Latinoamericana",
        "I": "Indígena americana", "J": "Japonesa", "K": "Coreana",
        "O": "Otros", "P": "Isleña del Pacífico", "S": "Samoana",
        "U": "Hawaiana", "V": "Vietnamita", "W": "Blanca",
        "X": "Desconocida", "Z": "Asiático indio"
    }
    descents_raw = sorted(df["Vict_Descent"].dropna().unique().tolist())
    descents = [{"code": c, "label": descents_map.get(c, c)} for c in descents_raw]
    
    return {
        "areas": areas,
        "descents": descents,
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
        crimen = fetch_user_case_by_id(id)
    if crimen is None:
        error_404(f"No se encontro ningun crimen ni caso de usuario con ID {id}")

    try:
        # Normalización de datos para los servicios
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
 