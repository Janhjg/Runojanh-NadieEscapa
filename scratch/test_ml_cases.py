import pandas as pd
import sys
import os

sys.path.append(os.getcwd())

from services.dataset_services import df

print("Loaded DF, length:", len(df) if df is not None else 0, flush=True)

if df is None or len(df) == 0:
    print("Dataset vacío → no se ejecuta test", flush=True)
    cases = []
else:
    cases = df.sample(min(10, len(df))).to_dict(orient="records")

from services.zero_shot_classification_service import construir_clasificacion

success = 0
failed = 0

for i, record in enumerate(cases):


    record_clean = {k: (None if pd.isna(v) else v) for k, v in record.items()}

    datos_modelo = {
        "DATE OCC":      record_clean.get("DATE_OCC") or record_clean.get("DATE OCC") or "",
        "TIME OCC":      record_clean.get("TIME_OCC") or record_clean.get("TIME OCC") or 0,
        "AREA NAME":     record_clean.get("AREA_NAME") or record_clean.get("AREA NAME") or "",
        "Rpt Dist No":   record_clean.get("Rpt_Dist_No") or record_clean.get("Rpt Dist No") or 0,
        "Part 1-2":      record_clean.get("Part_1_2") or record_clean.get("Part 1-2") or 2,
        "Crm Cd Desc":   record_clean.get("Crm_Cd_Desc") or record_clean.get("Crm Cd Desc") or "",
        "Vict Age":      record_clean.get("Vict_Age") or record_clean.get("Vict Age") or 0,
        "Vict Sex":      record_clean.get("Vict_Sex") or record_clean.get("Vict Sex") or "X",
        "Vict Descent":  record_clean.get("Vict_Descent") or record_clean.get("Vict Descent") or "X",
        "Premis Desc":   record_clean.get("Premis_Desc") or record_clean.get("Premis Desc") or "",
        "Weapon Desc":   record_clean.get("Weapon_Desc") or record_clean.get("Weapon Desc"),
        "Crm Cd 2 Desc": record_clean.get("Crm_Cd_2_Desc") or record_clean.get("Crm Cd 2 Desc"),
        "Crm Cd 3 Desc": record_clean.get("Crm_Cd_3_Desc") or record_clean.get("Crm Cd 3 Desc"),
        "Crm Cd 4 Desc": record_clean.get("Crm_Cd_4_Desc") or record_clean.get("Crm Cd 4 Desc"),
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

        continue

print(f"HF Test: {success} success, {failed} failed", flush=True)