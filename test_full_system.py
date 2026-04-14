from services.ml_service import predict
from services.zero_shot_classification_service import construir_clasificacion
from services.generator_service import generar_cronica

def test_case(name, data):
    print(f"\n{'='*20} Testing Case: {name} {'='*20}")
    
    # 1. Prediction
    pred = predict(data)
    print(f"Prediction: {pred['clase_predicha']} (Conf: {pred['confianza']})")
    
    # 2. Classification
    clas = construir_clasificacion(data, VObjetiva=pred['clase_predicha'])
    print(f"Top 1 Label (Context): {clas['etiqueta']['labels_contexto_clasificacion']}")
    print(f"Top 1 Label (Gen): {clas['etiqueta']['labels_genericas']}")
    
    # 3. Narrative Snippet
    cronica = generar_cronica(data, pred, clas['todas_etiquetas'])
    print(f"Narrative Preview: {cronica[:150]}...")

# Case 1: Child Murder with Vehicle (The user's case)
case_child = {
    "DATE OCC": "01/01/2024",
    "TIME OCC": 1200,
    "AREA NAME": "Central",
    "Rpt Dist No": 100,
    "Part 1-2": 1,
    "Crm Cd Desc": "HOMICIDE",
    "Vict Age": 10,
    "Vict Sex": "F",
    "Vict Descent": "H",
    "Premis Desc": "STREET",
    "Weapon Desc": "VEHICLE",
    "Status Desc": "Investigating"
}

# Case 2: Adult Battery with Hands
case_battery = {
    "DATE OCC": "01/01/2024",
    "TIME OCC": 2200,
    "AREA NAME": "Hollywood",
    "Rpt Dist No": 600,
    "Part 1-2": 2,
    "Crm Cd Desc": "BATTERY - SIMPLE ASSAULT",
    "Vict Age": 45,
    "Vict Sex": "M",
    "Vict Descent": "W",
    "Premis Desc": "SIDEWALK",
    "Weapon Desc": "STRONG-ARM (HANDS, FIST, FEET OR BODILY FORCE)",
    "Status Desc": "Adult Arrest"
}

if __name__ == "__main__":
    test_case("Homicide Kid", case_child)
    test_case("Simple Battery", case_battery)
