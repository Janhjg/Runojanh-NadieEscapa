import pandas as pd
import sys
import os

sys.path.append(os.getcwd())
from services.ml_service import predict

datos_modelo = {
    "DATE OCC":      "",
    "TIME OCC":      None,
    "AREA NAME":     None,
    "Rpt Dist No":   None,
    "Part 1-2":      None,
    "Crm Cd Desc":   None,
    "Vict Age":      None,
    "Vict Sex":      None,
    "Vict Descent":  None,
    "Premis Desc":   None,
    "Weapon Desc":   None,
    "Crm Cd 2 Desc": None,
    "Crm Cd 3 Desc": None,
    "Crm Cd 4 Desc": None,
}

try:
    pred = predict(datos_modelo)
    print("SUCCESS with None values!")
except Exception as e:
    print("FAILED with None values:", repr(e))
    import traceback
    traceback.print_exc()

datos_modelo_2 = {
    "DATE OCC":      "2023-01-01 12:00:00",
    "TIME OCC":      1200,
    "AREA NAME":     "Central",
    "Rpt Dist No":   123,
    "Part 1-2":      1,
    "Crm Cd Desc":   "ASSAULT",
    "Vict Age":      None, # What if just age is missing?
    "Vict Sex":      "M",
    "Vict Descent":  "H",
    "Premis Desc":   "STREET",
    "Weapon Desc":   "GUN",
    "Crm Cd 2 Desc": None,
    "Crm Cd 3 Desc": None,
    "Crm Cd 4 Desc": None,
}

try:
    pred = predict(datos_modelo_2)
    print("SUCCESS with just Age=None!")
except Exception as e:
    print("FAILED with just Age=None:", repr(e))

