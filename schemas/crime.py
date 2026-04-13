from pydantic import BaseModel, Field
from typing import Optional
 
 
class CrimeBase(BaseModel):
    model_config = {"from_attributes": True}
 
    DR_NO: Optional[int] = None
    DATE_OCC: Optional[str] = None
    TIME_OCC: Optional[int] = None
    AREA: Optional[int] = None
    AREA_NAME: Optional[str] = None
    Rpt_Dist_No: Optional[int] = None
    Part_1_2: Optional[int] = None
    Crm_Cd: Optional[int] = None
    Crm_Cd_Desc: Optional[str] = None
    Vict_Age: Optional[int] = None
    Vict_Sex: Optional[str] = None
    Vict_Descent: Optional[str] = None
    Premis_Cd: Optional[int] = None
    Premis_Desc: Optional[str] = None
    Weapon_Used_Cd: Optional[int] = None
    Weapon_Desc: Optional[str] = None
    Status_Desc: Optional[str] = None
    Crm_Cd_2: Optional[int] = None
    Crm_Cd_3: Optional[int] = None
    Crm_Cd_4: Optional[int] = None
    LOCATION: Optional[str] = None
    LAT: Optional[float] = None
    LON: Optional[float] = None
 
class CrimeListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    crimes: list[dict]
 
 
class CrimeDetailResponse(BaseModel):
    pass

    
    