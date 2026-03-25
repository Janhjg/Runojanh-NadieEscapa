from pydantic import BaseModel, Field
from typing import Optional

class CrimeBase(BaseModel):
    DR_NO: int = Field(..., description="Numero de reporte unico del crimen", example=220109275)
    DATE_OCC: str = Field(..., description="Fecha en que ocurrio el crimen", example="01/08/2022 12:00:00 AM")
    TIME_OCC: int = Field(..., description="Hora del crimen en formato 24h (HHMM)", example=2130)
    AREA_NAME: str = Field(..., description="Division policial donde ocurrio", example="Central")
    CRM_CD_DESC: str = Field(..., description="Tipo de crimen principal", example="BATTERY - SIMPLE ASSAULT")
    CRM_CD_2_DESC: Optional[str] = Field(None, description="Tipo de crimen secundario si existe", example="INTIMATE PARTNER - SIMPLE ASSAULT")
    VICT_AGE: int = Field(..., description="Edad de la victima", example=34)
    VICT_SEX: str = Field(..., description="Sexo de la victima (M, F, X)", example="M")
    VICT_DESCENT: Optional[str] = Field(None, description="Codigo de origen etnico de la victima", example="H")
    PREMIS_DESC: str = Field(..., description="Lugar donde ocurrio el crimen", example="STREET")
    WEAPON_DESC: Optional[str] = Field(None, description="Arma usada si existe", example="STRONG-ARM")
    STATUS_DESC: str = Field(..., description="Estado actual del caso", example="Invest Cont")
    PART_1_2: int = Field(..., description="Gravedad del crimen (1=grave, 2=leve)", example=1)
    LOCATION: str = Field(..., description="Direccion redondeada al bloque", example="700 W 6TH ST")
    LAT: float = Field(..., description="Latitud geografica", example=34.0522)
    LON: float = Field(..., description="Longitud geografica", example=-118.2437)
 
 
class CrimeListResponse(BaseModel):
    total: int = Field(..., description="Total de registros en el dataset", example=650000)
    limit: int = Field(..., description="Limite de registros devueltos", example=20)
    offset: int = Field(..., description="Desplazamiento desde el inicio", example=0)
    crimes: list[CrimeBase] = Field(..., description="Lista de crimenes")
 
 
class CrimeDetailResponse(CrimeBase):
    pass

    
    