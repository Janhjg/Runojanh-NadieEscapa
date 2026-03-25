from pydantic import BaseModel, Field
from .predict import PredictNewInput, PredictOutput
 
 
class ClassifyInput(BaseModel):
    datos_crimen: PredictNewInput = Field(..., description="Datos del crimen a clasificar")
    prediccion_ml: PredictOutput = Field(..., description="Prediccion del modelo ML previa")
 
 
class EtiquetaScore(BaseModel):
    label: str = Field(..., description="Etiqueta narrativa sentimental", example="robo desesperado")
    score: float = Field(..., description="Score de confianza", example=0.61)
 
 
class ClassifyOutput(BaseModel):
    etiqueta: str = Field(..., description="Etiqueta narrativa ganadora", example="robo desesperado")
    confianza: float = Field(..., description="Confianza de la etiqueta ganadora", example=0.61)
    texto_construido: str = Field(..., description="Texto enviado al modelo HuggingFace")
    todas_etiquetas: list[EtiquetaScore] = Field(..., description="Lista completa de etiquetas ordenadas por score")
    modelo: str = Field(..., description="Modelo HuggingFace usado", example="facebook/bart-large-mnli")