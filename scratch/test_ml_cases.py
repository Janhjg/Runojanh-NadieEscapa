import pandas as pd
import sys
import os

sys.path.append(os.getcwd())
from services.dataset_services import df

print("Loaded DF, length:", len(df), flush=True)

cases = df.sample(10).to_dict(orient="records")

from services.zero_shot_classification_service import construir_clasificacion

success = 0
failed = 0

for i, record in enumerate(cases):
    record_clean = {k: (None if pd.isna(v) else v) for k, v in record.items()}
    datos_modelo = {
        "DATE OCC":      record_clean.get("DATE_OCC", record_clean.get("DATE OCC", "")),
        "TIME OCC":      record_clean.get("TIME_OCC", record_clean.get("TIME OCC", 0)),
        "AREA NAME":     record_clean.get("AREA_NAME", record_clean.get("AREA NAME", "")),
        "Rpt Dist No":   record_clean.get("Rpt_Dist_No", record_clean.get("Rpt Dist No", 0)),
        "Part 1-2":      record_clean.get("Part_1_2", record_clean.get("Part 1-2", 2)),
        "Crm Cd Desc":   record_clean.get("Crm_Cd_Desc", record_clean.get("Crm Cd Desc", "")),
        "Vict Age":      record_clean.get("Vict_Age", record_clean.get("Vict Age", 0)),
        "Vict Sex":      record_clean.get("Vict_Sex", record_clean.get("Vict Sex", "X")),
        "Vict Descent":  record_clean.get("Vict_Descent", record_clean.get("Vict Descent", "X")),
        "Premis Desc":   record_clean.get("Premis_Desc", record_clean.get("Premis Desc", "")),
        "Weapon Desc":   record_clean.get("Weapon_Desc", record_clean.get("Weapon Desc", None)),
        "Crm Cd 2 Desc": record_clean.get("Crm_Cd_2_Desc", record_clean.get("Crm Cd 2 Desc", None)),
        "Crm Cd 3 Desc": record_clean.get("Crm_Cd_3_Desc", record_clean.get("Crm Cd 3 Desc", None)),
        "Crm Cd 4 Desc": record_clean.get("Crm_Cd_4_Desc", record_clean.get("Crm Cd 4 Desc", None)),
    }
    
    try:
        clas = construir_clasificacion(datos_modelo, VObjetiva="arrestado")
        success += 1
        print(f"HF success {i}", flush=True)
    except Exception as e:
        print(f"Case {record_clean.get('DR_NO')} failed CLASSIFY:", repr(e), flush=True)
        import traceback
        traceback.print_exc()
        failed += 1
        break

print(f"HF Test: {success} success, {failed} failed", flush=True)
