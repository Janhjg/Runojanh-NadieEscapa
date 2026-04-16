import requests
import json
import sys

# ID de ejemplo que debería existir en el dataset (DR_NO)
CRIME_ID = 220109275 
URL = f"http://localhost:8001/full-case/{CRIME_ID}"

def test_full_case_by_id():
    try:
        print(f"Enviando peticion GET a {URL}...")
        response = requests.get(URL)
        
        if response.status_code == 200:
            print("SUCCESS!")
            data = response.json()
            
            print(f"\n--- DATOS DEL CRIMEN (ID: {data['id']}) ---")
            print(f"Tipo: {data['datos_caso']['Crm_Cd_Desc']}")
            print(f"Lugar: {data['datos_caso']['Premis_Desc']}")
            
            print("\n--- ML PREDICTION ---")
            print(f"Clase: {data['prediccion_ml']['clase_predicha']}")
            print(f"Confianza: {data['prediccion_ml']['confianza']}")
            
            print("\n--- HF CLASSIFICATION ---")
            print(f"Etiquetas: {data['clasificacion_hf']['etiqueta']}")
            
            print("\n--- NOIR CHRONICLE ---")
            print(data['cronica'])
            
            print("\n--- MODEL USE ---")
            print(f"Generativo: {data['tecnologias']['ia_generativa']}")
            
        elif response.status_code == 404:
            print(f"FAILED: El crimen con ID {CRIME_ID} no existe en el dataset.")
        else:
            print(f"FAILED with status code: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error connecting to server: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        CRIME_ID = sys.argv[1]
        URL = f"http://localhost:8001/full-case/{CRIME_ID}"
    test_full_case_by_id()
