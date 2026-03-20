from pydantic import BaseModel, Field
from .predict import PredictNewInput, PredictOutput
 
 
class NarrateInput(BaseModel):
    datos_crimen: PredictNewInput = Field(..., description="Datos del crimen a narrar")
    prediccion_ml: PredictOutput = Field(..., description="Prediccion del modelo ML")
    etiqueta_huggingface: str = Field(..., description="Etiqueta narrativa de HuggingFace", example="robo desesperado")
 
 
class NarrateOutput(BaseModel):
    cronica: str = Field(..., description="Cronica de novela negra generada por la IA")
    palabras: int = Field(..., description="Numero de palabras de la cronica", example=247)
    etiqueta_usada: str = Field(..., description="Etiqueta narrativa usada para el tono", example="robo desesperado")
    clase_predicha_usada: str = Field(..., description="Clase predicha usada en la narracion", example="no arrestado")
    modelo: str = Field(..., description="Modelo de IA Generativa usado", example="gemini-2.0-flash")