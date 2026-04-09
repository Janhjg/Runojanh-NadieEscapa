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

def get_all_crimes(
    limit: int = 20,
    offset: int = 0,
    area: int | None = None,
    crm_cd: int | None = None,
    part_1_2: int | None = None,
    vict_sex: str | None = None,
    vict_descent: str | None = None,
    premis_cd: int | None = None,
    weapon_used_cd: int | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
) -> dict:

    if df.empty:
        return {
            "total": 0,
            "limit": limit,
            "offset": offset,
            "filters_applied": {},
            "crimes": []
        }

    filtered = df.copy()

    # ── Aplicar filtros solo si se reciben ────────────────────
    try:
        if area is not None:
            filtered = filtered[filtered["AREA"] == area]

        if crm_cd is not None:
            filtered = filtered[filtered["Crm_Cd"] == crm_cd]

        if part_1_2 is not None:
            filtered = filtered[filtered["Part_1_2"] == part_1_2]

        if vict_sex is not None:
            filtered = filtered[filtered["Vict_Sex"].astype(str).str.upper() == vict_sex.upper()]

        if vict_descent is not None:
            filtered = filtered[filtered["Vict_Descent"].astype(str).str.upper() == vict_descent.upper()]

        if premis_cd is not None:
            filtered = filtered[filtered["Premis_Cd"] == premis_cd]

        if weapon_used_cd is not None:
            filtered = filtered[filtered["Weapon_Used_Cd"] == weapon_used_cd]

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

    except KeyError as e:
        print(f"Columna no encontrada al filtrar: {e}")

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
        "filters_applied": {
            k: v for k, v in {
                "area": area,
                "crm_cd": crm_cd,
                "part_1_2": part_1_2,
                "vict_sex": vict_sex,
                "vict_descent": vict_descent,
                "premis_cd": premis_cd,
                "weapon_used_cd": weapon_used_cd,
                "date_from": date_from,
                "date_to": date_to,
            }.items() if v is not None
        },
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


def delete_user_case(user_case_id: int) -> bool:
    global user_cases
    original   = len(user_cases)
    user_cases = [c for c in user_cases if c["user_case_id"] != user_case_id]
    return len(user_cases) < original