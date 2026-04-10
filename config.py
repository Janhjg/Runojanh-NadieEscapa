from pydantic_settings import BaseSettings
from pathlib import Path
 
BASE_DIR = Path(__file__).resolve().parent.parent
 
 
class Settings(BaseSettings):
 
    # ── API ───────────────────────────────────────────────────
    APP_NAME: str = "Runojanh - The Dark Chronicles"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = (
        "API que transforma crimenes urbanos reales en narrativas "
        "de novela negra usando ML, HuggingFace y IA Generativa."
    )
    DEBUG: bool = False
 
    # ── Dataset ───────────────────────────────────────────────
    DATA_RAW_PATH: Path = BASE_DIR / "data" / "raw" / "crime_data.csv"
    DATA_PROCESSED_PATH: Path = BASE_DIR / "data" / "processed" / "clean_dataset.csv"
 
    # ── Modelo ML ─────────────────────────────────────────────
    ML_DIR: Path = BASE_DIR / "ml"
    MODEL_PATH: Path = BASE_DIR / "ml" / "model.joblib"
    LE_AREA_PATH: Path = BASE_DIR / "ml" / "le_area.joblib"
    LE_CRM_PATH: Path = BASE_DIR / "ml" / "le_crm.joblib"
    LE_CRM2_PATH: Path = BASE_DIR / "ml" / "le_crm2.joblib"
    LE_SEX_PATH: Path = BASE_DIR / "ml" / "le_sex.joblib"
    LE_PREMIS_PATH: Path = BASE_DIR / "ml" / "le_premis.joblib"
    LE_WEAPON_PATH: Path = BASE_DIR / "ml" / "le_weapon.joblib"
 
    # ── HuggingFace ───────────────────────────────────────────
    HF_MODEL: str = "facebook/bart-large-mnli"
    HF_ETIQUETAS: list[str] = [
        "crimen pasional",
        "robo desesperado",
        "venganza organizada",
        "ataque oportunista",
        "crimen del hampa",
        "tragedia urbana",
        "ajuste de cuentas",
        "violencia sin salida"
    ]