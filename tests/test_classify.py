import requests
import json

URL = "http://localhost:8003/classify"



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
    },
    "prediccion_ml": {
        "clase_predicha": "arrestado",
        "probabilidad_arrestado": 0.9,
        "probabilidad_no_arrestado": 0.1,
        "confianza": 0.9,
        "modelo": "RandomForestClassifier"
    }
}

def test_classify():
    try:
        print(f"Enviando peticion a {URL}...")
        response = requests.post(URL, json=payload)
        
        if response.status_code == 200:
            print("SUCCESS!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"FAILED with status code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error connecting to server: {e}")

if __name__ == "__main__":
    test_classify()
