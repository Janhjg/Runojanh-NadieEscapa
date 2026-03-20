from pydantic import BaseModel, Field
from .crime import CrimeBase
from .predict import PredictNewInput, PredictOutput
from .classify import ClassifyOutput
 
 
class FullCaseNewInput(BaseModel):
    datos_crimen: PredictNewInput = Field(..., description="Datos del crimen introducidos manualmente")
 
 
class FullCaseOutput(BaseModel):
    datos_caso: PredictNewInput = Field(..., description="Datos del crimen procesado")
    prediccion_ml: PredictOutput = Field(..., description="Resultado del modelo ML")
    clasificacion_hf: ClassifyOutput = Field(..., description="Resultado del modelo HuggingFace")
    cronica: str = Field(..., description="Cronica de novela negra generada")
    tecnologias: dict = Field(
        default={
            "ml": "RandomForestClassifier (scikit-learn)",
            "huggingface": "facebook/bart-large-mnli (zero-shot-classification)",
            "ia_generativa": "gemini-2.0-flash (Google)"
        },
        description="Tecnologias usadas en la generacion"
    )
 
 
class FullCaseByIdOutput(BaseModel):
    id: int = Field(..., description="ID del crimen en el dataset", example=220109275)
    datos_caso: CrimeBase = Field(..., description="Datos completos del crimen del dataset")
    prediccion_ml: PredictOutput = Field(..., description="Resultado del modelo ML")
    clasificacion_hf: ClassifyOutput = Field(..., description="Resultado del modelo HuggingFace")
    cronica: str = Field(..., description="Cronica de novela negra generada")
    tecnologias: dict = Field(
        default={
            "ml": "RandomForestClassifier (scikit-learn)",
            "huggingface": "facebook/bart-large-mnli (zero-shot-classification)",
            "ia_generativa": "gemini-2.0-flash (Google)"
        },
        description="Tecnologias usadas en la generacion"
    )