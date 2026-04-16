
from pathlib import Path
import pandas as pd
import os

BASE_DIR  = Path(os.getcwd())
DATA_PATH = BASE_DIR / "data" / "crimeData_limpio.csv"

print(f"Checking data at {DATA_PATH}")
if DATA_PATH.exists():
    print("File exists. Loading...")
    try:
        df = pd.read_csv(DATA_PATH, low_memory=False, nrows=100)
        print("Success! Head:")
        print(df.head())
    except Exception as e:
        print(f"Error: {e}")
else:
    print("File DOES NOT exist.")
