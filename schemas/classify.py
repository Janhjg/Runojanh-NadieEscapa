
from pydantic import BaseModel, Field
from .predict import PredictNewInput, PredictOutput

class ClassifyInput(BaseModel):
    datos_crimen: PredictNewInput = Field(..., description="Datos del crimen a clasificar")
    prediccion_ml: PredictOutput  = Field(..., description="Prediccion del modelo ML previa")


class EtiquetaScore(BaseModel):
    label: str   = Field(..., description="Etiqueta narrativa", example="disparo")
    score: float = Field(..., description="Score de confianza", example=0.61)


class ClassifyOutput(BaseModel):
    # ✅ etiqueta ganadora por categoría
    etiqueta: dict[str, str] = Field(
        ..., description="Label #1 por categoría",
        example={"labels_genericas": "frío", "labels_motivo_crimen": "disparo"}
    )
    # ✅ confianza ganadora por categoría
    confianza: dict[str, float] = Field(
        ..., description="Score del label ganador por categoría",
        example={"labels_genericas": 0.87}
    )
    texto_construido: str = Field(..., description="Texto enviado al modelo HuggingFace")
    # ✅ tipo correcto: dict[str, list[EtiquetaScore]]
    todas_etiquetas: dict[str, list[EtiquetaScore]] = Field(
        ..., description="Etiquetas con scores por categoría"
    )
    modelo: str = Field(..., description="Modelo HuggingFace usado", example="facebook/bart-large-mnli")