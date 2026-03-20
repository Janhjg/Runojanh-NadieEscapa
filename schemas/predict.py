from pydantic import BaseModel, Field
from typing import Optional
from .crime import CrimeBase
 
 
class PredictNewInput(BaseModel):
    AREA_NAME: str = Field(..., description="Division policial donde ocurrio el crimen", example="Central")
    CRM_CD_DESC: str = Field(..., description="Tipo de crimen principal", example="BATTERY - SIMPLE ASSAULT")
    CRM_CD_2_DESC: Optional[str] = Field(None, description="Tipo de crimen secundario si existe", example="INTIMATE PARTNER - SIMPLE ASSAULT")
    VICT_AGE: int = Field(..., ge=0, le=120, description="Edad de la victima", example=34)
    VICT_SEX: str = Field(..., description="Sexo de la victima (M, F, X)", example="M")
    PREMIS_DESC: str = Field(..., description="Lugar donde ocurrio el crimen", example="STREET")
    WEAPON_DESC: Optional[str] = Field(None, description="Arma usada si existe", example="STRONG-ARM")
    PART_1_2: int = Field(..., ge=1, le=2, description="Gravedad del crimen (1=grave, 2=leve)", example=1)
    hour: int = Field(..., ge=0, le=23, description="Hora en que ocurrio el crimen", example=21)
    month: int = Field(..., ge=1, le=12, description="Mes en que ocurrio el crimen", example=1)
    day_of_week: int = Field(..., ge=0, le=6, description="Dia de la semana (0=lunes, 6=domingo)", example=4)
 
 
class PredictOutput(BaseModel):
    clase_predicha: str = Field(..., description="Clase predicha por el modelo", example="no arrestado")
    probabilidad_arrestado: float = Field(..., description="Probabilidad de arresto", example=0.18)
    probabilidad_no_arrestado: float = Field(..., description="Probabilidad de no arresto", example=0.82)
    confianza: float = Field(..., description="Confianza del modelo", example=0.82)
    modelo: str = Field(..., description="Modelo ML usado", example="RandomForestClassifier")
 
 
class PredictByIdResponse(BaseModel):
    id: int = Field(..., description="ID del crimen en el dataset", example=220109275)
    datos_caso: CrimeBase = Field(..., description="Datos completos del crimen")
    prediccion: PredictOutput = Field(..., description="Resultado de la prediccion ML")