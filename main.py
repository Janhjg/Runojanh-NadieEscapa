from fastapi import FastAPI
from datetime import datetime
 
from schemas import (
    CrimeListResponse, CrimeDetailResponse,
    PredictNewInput, PredictOutput, PredictByIdResponse,
    ClassifyInput, ClassifyOutput,
    NarrateInput, NarrateOutput,
    FullCaseNewInput, FullCaseOutput, FullCaseByIdOutput
)
from services import error_400, error_404, error_422, error_503, error_504

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
 
@app.get("/crimes", response_model=CrimeListResponse, tags=["Dataset"])
def get_crimes(limit: int = 20, offset: int = 0):
    if limit <= 0 or offset < 0:
        error_422("limit debe ser mayor que 0 y offset no puede ser negativo")
 
 
@app.get("/crimes/{id}", response_model=CrimeDetailResponse, tags=["Dataset"])
def get_crime_by_id(id: int):
    if id <= 0:
        error_422("El ID debe ser un numero positivo")
 
 
# ML
 
@app.post("/predict/new", response_model=PredictOutput, tags=["ML"])
def predict_new(data: PredictNewInput):
    pass
 
 
@app.get("/predict/{id}", response_model=PredictByIdResponse, tags=["ML"])
def predict_by_id(id: int):
    if id <= 0:
        error_422("El ID debe ser un numero positivo")
 
 
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
 