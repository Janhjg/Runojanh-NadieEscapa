from pydantic import BaseModel, Field
from typing import Optional
from .crime import CrimeBase
 
 
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from .crime import CrimeBase


class PredictNewInput(BaseModel):
    """
    Datos que el usuario rellena para predecir un caso nuevo.
    Usa nombres descriptivos que el ml_service mapea internamente.
    """
    model_config = ConfigDict(populate_by_name=True)

    DATE_OCC: str = Field(
        ...,
        alias="DATE OCC",
        description="Fecha del crimen",
        json_schema_extra="01/08/2022 12:00:00 AM"
    )
    TIME_OCC: int = Field(
        ...,
        alias="TIME OCC",
        description="Hora del crimen en formato militar HHMM",
        json_schema_extra=2130
    )
    AREA_NAME: str = Field(
        ...,
        alias="AREA NAME",
        description="Division policial donde ocurrio el crimen",
        json_schema_extra="Central"
    )
    Rpt_Dist_No: int = Field(
        ...,
        alias="Rpt Dist No",
        description="Numero de sector del barrio",
        json_schema_extra=122
    )
    Part_1_2: int = Field(
        ...,
        alias="Part 1-2",
        ge=1, le=2,
        description="Gravedad del crimen (1=grave, 2=leve)",
        json_schema_extra=1
    )
    Crm_Cd_Desc: str = Field(
        ...,
        alias="Crm Cd Desc",
        description="Descripcion del tipo de crimen principal",
        json_schema_extra="BATTERY - SIMPLE ASSAULT"
    )
    Vict_Age: int = Field(
        ...,
        alias="Vict Age",
        ge=0, le=120,
        description="Edad de la victima",
        json_schema_extra=34
    )
    Vict_Sex: str = Field(
        ...,
        alias="Vict Sex",
        description="Sexo de la victima (M=Hombre, F=Mujer, X=Desconocido)",
        json_schema_extra="M"
    )
    Vict_Descent: Optional[str] = Field(
        None,
        alias="Vict Descent",
        description="Codigo de descendencia de la victima (H=Hispano, W=Blanco, B=Negro...)",
        json_schema_extra="H"
    )
    Premis_Desc: str = Field(
        ...,
        alias="Premis Desc",
        description="Lugar donde ocurrio el crimen",
        json_schema_extra="STREET"
    )
    Weapon_Desc: Optional[str] = Field(
        None,
        alias="Weapon Desc",
        description="Descripcion del arma usada si existe",
        json_schema_extra="STRONG-ARM (HANDS, FIST, FEET OR BODILY FORCE)"
    )
    Crm_Cd_2_Desc: Optional[str] = Field(
        None,
        alias="Crm Cd 2 Desc",
        description="Descripcion del crimen secundario si existe",
        json_schema_extra="INTIMATE PARTNER - SIMPLE ASSAULT"
    )
    Crm_Cd_3_Desc: Optional[str] = Field(
        None,
        alias="Crm Cd 3 Desc",
        description="Descripcion del crimen terciario si existe",
        json_schema_extra=None
    )
    Crm_Cd_4_Desc: Optional[str] = Field(
        None,
        alias="Crm Cd 4 Desc",
        description="Descripcion del crimen cuaternario si existe",
        json_schema_extra=None
    )


class PredictOutput(BaseModel):
    clase_predicha: str = Field(
        ...,
        description="Clase predicha por el modelo",
        json_schema_extra="no arrestado"
    )
    probabilidad_arrestado: float = Field(
        ...,
        description="Probabilidad de que el caso resulte en arresto",
        json_schema_extra=0.18
    )
    probabilidad_no_arrestado: float = Field(
        ...,
        description="Probabilidad de que el caso no resulte en arresto",
        json_schema_extra=0.82
    )
    confianza: float = Field(
        ...,
        description="Confianza del modelo en la prediccion",
        json_schema_extra=0.82
    )
    modelo: str = Field(
        ...,
        description="Modelo ML usado",
        json_schema_extra="RandomForestClassifier"
    )


class PredictByIdResponse(BaseModel):
    id: int = Field(
        ...,
        description="ID del crimen en el dataset",
        json_schema_extra=220109275
    )
    datos_caso: CrimeBase = Field(
        ...,
        description="Datos completos del crimen recuperado del dataset"
    )
    prediccion: PredictOutput = Field(
        ...,
        description="Resultado de la prediccion ML"
    )