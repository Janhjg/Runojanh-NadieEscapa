import pandas as pd
from pathlib import Path

# Carga del dataset al arrancar
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "clean_dataset.csv"

try:
    df = pd.read_csv(DATA_PATH)
    print(f"Dataset cargado: {len(df)} registros")
except FileNotFoundError:
    print("Dataset no encontrado. Carga el CSV en data/processed/")
    df = pd.DataFrame()


def get_crime_by_id(id: int) -> dict | None:
    if df.empty:
        return None

    resultado = df[df["DR_NO"] == id]

    if resultado.empty:
        return None

    return resultado.iloc[0].to_dict()


def get_all_crimes(limit: int, offset: int) -> dict:
    if df.empty:
        return {"total": 0, "limit": limit, "offset": offset, "crimes": []}

    total = len(df)
    subset = df.iloc[offset:offset + limit]
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "crimes": subset.to_dict(orient="records")
    }