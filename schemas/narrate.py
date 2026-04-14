from pydantic import BaseModel, Field
from .predict import PredictNewInput, PredictOutput
from .classify import EtiquetaScore
 
 
class NarrateInput(BaseModel):
    datos_crimen: PredictNewInput = Field(..., description="Datos del crimen a narrar")
    prediccion_ml: PredictOutput = Field(..., description="Prediccion del modelo ML")
    etiquetas_huggingface: dict[str, list[EtiquetaScore]] = Field(..., description="Etiquetas narrativas de HuggingFace por categoría")
 
 
class NarrateOutput(BaseModel):
    cronica: str = Field(..., description="Cronica de novela negra generada por la IA")
    palabras: int = Field(..., description="Numero de palabras de la cronica", example=247)
    etiquetas_usadas: dict[str, list[EtiquetaScore]] = Field(..., description="Etiquetas narrativas usadas para el tono")
    clase_predicha_usada: str = Field(..., description="Clase predicha usada en la narracion", example="no arrestado")
    modelo: str = Field(..., description="Modelo de IA Generativa usado", example="gemini-2.0-flash")