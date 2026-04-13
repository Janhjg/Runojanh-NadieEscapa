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
        example="01/08/2022 12:00:00 AM"
    )
    TIME_OCC: int = Field(
        ...,
        alias="TIME OCC",
        description="Hora del crimen en formato militar HHMM",
        example=2130
    )
    AREA_NAME: str = Field(
        ...,
        alias="AREA NAME",
        description="Division policial donde ocurrio el crimen",
        example="Central"
    )
    Rpt_Dist_No: int = Field(
        ...,
        alias="Rpt Dist No",
        description="Numero de sector del barrio",
        example=122
    )
    Part_1_2: int = Field(
        ...,
        alias="Part 1-2",
        ge=1, le=2,
        description="Gravedad del crimen (1=grave, 2=leve)",
        example=1
    )
    Crm_Cd_Desc: str = Field(
        ...,
        alias="Crm Cd Desc",
        description="Descripcion del tipo de crimen principal",
        example="BATTERY - SIMPLE ASSAULT"
    )
    Vict_Age: int = Field(
        ...,
        alias="Vict Age",
        ge=0, le=120,
        description="Edad de la victima",
        example=34
    )
    Vict_Sex: str = Field(
        ...,
        alias="Vict Sex",
        description="Sexo de la victima (M=Hombre, F=Mujer, X=Desconocido)",
        example="M"
    )
    Vict_Descent: Optional[str] = Field(
        None,
        alias="Vict Descent",
        description="Codigo de descendencia de la victima (H=Hispano, W=Blanco, B=Negro...)",
        example="H"
    )
    Premis_Desc: str = Field(
        ...,
        alias="Premis Desc",
        description="Lugar donde ocurrio el crimen",
        example="STREET"
    )
    Weapon_Desc: Optional[str] = Field(
        None,
        alias="Weapon Desc",
        description="Descripcion del arma usada si existe",
        example="STRONG-ARM (HANDS, FIST, FEET OR BODILY FORCE)"
    )
    Crm_Cd_2_Desc: Optional[str] = Field(
        None,
        alias="Crm Cd 2 Desc",
        description="Descripcion del crimen secundario si existe",
        example="INTIMATE PARTNER - SIMPLE ASSAULT"
    )
    Crm_Cd_3_Desc: Optional[str] = Field(
        None,
        alias="Crm Cd 3 Desc",
        description="Descripcion del crimen terciario si existe",
        example=None
    )
    Crm_Cd_4_Desc: Optional[str] = Field(
        None,
        alias="Crm Cd 4 Desc",
        description="Descripcion del crimen cuaternario si existe",
        example=None
    )


class PredictOutput(BaseModel):
    clase_predicha: str = Field(
        ...,
        description="Clase predicha por el modelo",
        example="no arrestado"
    )
    probabilidad_arrestado: float = Field(
        ...,
        description="Probabilidad de que el caso resulte en arresto",
        example=0.18
    )
    probabilidad_no_arrestado: float = Field(
        ...,
        description="Probabilidad de que el caso no resulte en arresto",
        example=0.82
    )
    confianza: float = Field(
        ...,
        description="Confianza del modelo en la prediccion",
        example=0.82
    )
    modelo: str = Field(
        ...,
        description="Modelo ML usado",
        example="RandomForestClassifier"
    )


class PredictByIdResponse(BaseModel):
    id: int = Field(
        ...,
        description="ID del crimen en el dataset",
        example=220109275
    )
    datos_caso: CrimeBase = Field(
        ...,
        description="Datos completos del crimen recuperado del dataset"
    )
    prediccion: PredictOutput = Field(
        ...,
        description="Resultado de la prediccion ML"
    )