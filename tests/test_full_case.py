import requests
import json

URL = "http://localhost:8001/full-case/new"

payload = {
    "datos_crimen": {
        "DATE OCC": "01/01/2023 12:00:00 AM",
        "TIME OCC": 1200,
        "AREA NAME": "Central",
        "Rpt Dist No": 101,
        "Part 1-2": 1,
        "Crm Cd Desc": "HOMICIDE",
        "Vict Age": 25,
        "Vict Sex": "M",
        "Vict Descent": "H",
        "Premis Desc": "STREET",
        "Weapon Desc": "HANDS"
    }
}

def test_full_case():
    try:
        print(f"Enviando peticion a {URL}...")
        response = requests.post(URL, json=payload)
        
        if response.status_code == 200:
            print("SUCCESS!")
            data = response.json()
            print("\n--- ML PREDICTION ---")
            print(f"Clase: {data['prediccion_ml']['clase_predicha']}")
            print(f"Confianza: {data['prediccion_ml']['confianza']}")
            
            print("\n--- HF CLASSIFICATION ---")
            print(f"Etiquetas: {data['clasificacion_hf']['etiqueta']}")
            
            print("\n--- NOIR CHRONICLE ---")
            print(data['cronica'])
            
            print("\n--- TECH STACK ---")
            print(json.dumps(data['tecnologias'], indent=2))
        else:
            print(f"FAILED with status code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error connecting to server: {e}")

if __name__ == "__main__":
    test_full_case()
