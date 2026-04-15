import requests
import json

URL = "http://localhost:8005/narrate"


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
    },
    "etiquetas_huggingface": {
        "labels_genericas": [{"label": "frío", "score": 0.9}, {"label": "calculado", "score": 0.8}],
        "labels_motivo_crimen": [{"label": "venganza", "score": 0.95}],
        "labels_escena_caracteristicas": [{"label": "limpia", "score": 0.85}, {"label": "sin huellas", "score": 0.7}, {"label": "tiro de gracia", "score": 0.9}],
        "labels_contexto_clasificacion": [{"label": "crimen organizado", "score": 0.9}, {"label": "profesional", "score": 0.8}]
    }
}

def test_narrate():
    try:
        print(f"Enviando peticion a {URL}...")
        response = requests.post(URL, json=payload)
        
        if response.status_code == 200:
            print("SUCCESS!")
            data = response.json()
            print(f"Cronica:\n{data['cronica']}")
            print(f"Palabras: {data['palabras']}")
        else:
            print(f"FAILED with status code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error connecting to server: {e}")

if __name__ == "__main__":
    test_narrate()
