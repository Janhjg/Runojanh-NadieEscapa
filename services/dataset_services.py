import pandas as pd
from pathlib import Path
from datetime import datetime

# ── Carga del dataset ─────────────────────────────────────────
BASE_DIR  = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "crimeData_limpio.csv"

try:
    df = pd.read_csv(DATA_PATH, low_memory=False)
    # Limpiar nombres de columnas — quitar espacios y guiones
    df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace("-", "_")
    # Rellenar nulos en columnas opcionales con 0 o cadena vacia
    df = df.fillna(0)
    print(f"Dataset cargado: {len(df)} registros")
    print(f"Columnas disponibles: {list(df.columns)}")
except FileNotFoundError:
    print("Dataset no encontrado. Carga el CSV en data/processed/")
    df = pd.DataFrame()

# ── Almacen de casos nuevos creados por el usuario ────────────
user_cases: list[dict] = []
user_case_counter: int = 1


# ══════════════════════════════════════════════════════════════
# DATASET ORIGINAL
# ══════════════════════════════════════════════════════════════

def get_filtered_df(
    area: int | None = None,
    crm_cd: int | None = None,
    part_1_2: int | None = None,
    vict_sex: str | None = None,
    vict_descent: str | None = None,
    premis_cd: int | None = None,
    weapon_used_cd: int | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    area_name: str | None = None,
    crime_desc: str | None = None,
    vict_age_min: int | None = None,
    vict_age_max: int | None = None,
    time_occ_min: int | None = None,
    time_occ_max: int | None = None,
    status_desc: str | None = None,
    weapon_desc: str | None = None,
    premis_desc: str | None = None,
    dr_no: int | None = None,
) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    filtered = df.copy()

    try:
        if dr_no is not None:
            filtered = filtered[filtered["DR_NO"] == dr_no]

        if area is not None:
            filtered = filtered[filtered["AREA"] == area]
        
        if area_name is not None:
            filtered = filtered[filtered["AREA_NAME"].astype(str).str.contains(area_name, case=False, na=False)]

        if crime_desc is not None:
            filtered = filtered[filtered["Crm_Cd_Desc"].astype(str).str.contains(crime_desc, case=False, na=False)]

        if crm_cd is not None:
            filtered = filtered[filtered["Crm_Cd"] == crm_cd]

        if part_1_2 is not None:
            filtered = filtered[filtered["Part_1_2"] == part_1_2]

        if vict_sex is not None:
            filtered = filtered[filtered["Vict_Sex"].astype(str).str.upper() == vict_sex.upper()]

        if vict_descent is not None:
            filtered = filtered[filtered["Vict_Descent"].astype(str).str.upper() == vict_descent.upper()]

        if status_desc is not None:
            filtered = filtered[filtered["Status_Desc"].astype(str).str.contains(status_desc, case=False, na=False)]

        if weapon_desc is not None:
            filtered = filtered[filtered["Weapon_Desc"].astype(str).str.contains(weapon_desc, case=False, na=False)]

        if premis_desc is not None:
            filtered = filtered[filtered["Premis_Desc"].astype(str).str.contains(premis_desc, case=False, na=False)]

        if premis_cd is not None:
            filtered = filtered[filtered["Premis_Cd"] == premis_cd]

        if weapon_used_cd is not None:
            filtered = filtered[filtered["Weapon_Used_Cd"] == weapon_used_cd]

        if vict_age_min is not None:
            filtered = filtered[filtered["Vict_Age"] >= int(vict_age_min)]
        
        if vict_age_max is not None:
            filtered = filtered[filtered["Vict_Age"] <= int(vict_age_max)]

        if time_occ_min is not None:
            filtered = filtered[filtered["TIME_OCC"] >= int(time_occ_min)]
        
        if time_occ_max is not None:
            filtered = filtered[filtered["TIME_OCC"] <= int(time_occ_max)]

        if date_from is not None:
            filtered = filtered[
                pd.to_datetime(filtered["DATE_OCC"], dayfirst=False, errors="coerce") >=
                pd.to_datetime(date_from, dayfirst=False, errors="coerce")
            ]

        if date_to is not None:
            filtered = filtered[
                pd.to_datetime(filtered["DATE_OCC"], dayfirst=False, errors="coerce") <=
                pd.to_datetime(date_to, dayfirst=False, errors="coerce")
            ]

    except Exception as e:
        print(f"Error al filtrar: {e}")

    return filtered

def get_unique_values(column: str) -> list:
    if df.empty or column not in df.columns:
        return []
    return sorted([str(x) for x in df[column].unique() if pd.notna(x)])

def get_all_crimes(
    limit: int = 20,
    offset: int = 0,
    **filters
) -> dict:

    filtered = get_filtered_df(**filters)
    
    if filtered.empty and not df.empty and any(v is not None for v in filters.values()):
         # Si hay filtros y no hay resultados
         return {
            "total": 0,
            "limit": limit,
            "offset": offset,
            "filters_applied": {k: v for k, v in filters.items() if v is not None},
            "crimes": []
        }

    total  = len(filtered)
    subset = filtered.iloc[offset:offset + limit]

    # ── Convertir a lista de dicts limpia ─────────────────────
    crimes = []
    for record in subset.to_dict(orient="records"):
        cleaned = {
            k: (None if pd.isna(v) else v)
            for k, v in record.items()
        }
        crimes.append(cleaned)

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "filters_applied": {k: v for k, v in filters.items() if v is not None},
        "crimes": crimes
    }


def fetch_crime_by_id(id: int) -> dict | None:
    """Busca un crimen del dataset por DR_NO."""
    if df.empty:
        return None

    resultado = df[df["DR_NO"] == id]

    if resultado.empty:
        return None

    record = resultado.iloc[0].to_dict()
    return {k: (None if pd.isna(v) else v) for k, v in record.items()}


# ══════════════════════════════════════════════════════════════
# CASOS NUEVOS CREADOS POR EL USUARIO
# ══════════════════════════════════════════════════════════════

def create_user_case(data: dict) -> dict:
    global user_case_counter

    nuevo_caso = {
        "user_case_id": user_case_counter,
        "created_at": datetime.now().isoformat(),
        "source": "usuario",
        **data
    }

    user_cases.append(nuevo_caso)
    user_case_counter += 1

    return nuevo_caso


def get_all_user_cases(limit: int, offset: int) -> dict:
    total  = len(user_cases)
    subset = user_cases[offset:offset + limit]

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "source": "usuario",
        "cases": subset
    }


def fetch_user_case_by_id(user_case_id: int) -> dict | None:
    for case in user_cases:
        if case["user_case_id"] == user_case_id:
            return case
    return None

def update_user_case(user_case_id: int, updates: dict) -> bool:
    for case in user_cases:
        if case["user_case_id"] == user_case_id:
            case.update(updates)
            return True
    return False

def delete_user_case(user_case_id: int) -> bool:
    global user_cases
    original   = len(user_cases)
    user_cases = [c for c in user_cases if c["user_case_id"] != user_case_id]
    return len(user_cases) < original