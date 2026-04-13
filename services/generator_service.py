import os
import sys
from ollama import chat
from ollama import ChatResponse



script="Actúa como un novelista experto en género noir y hardboiled. Quiero desarrollar una historia basada en el siguiente caso criminal te pasaré algunos datos en ingles, traducelo: 'Description of Crime:THEFT OF IDENTITY, Nivel:2, Weapon:UNKNOWN WEAPON/OTHER WEAPON , el dia 07/22/2020 12:00:00 AM, a la hora 1200, en Wilshire, distrito:775, in a MULTI-UNIT DWELLING (APARTMENT, DUPLEX, ETC). Información de la victima: edad= 35, sexo=Femenino descendencia=negra, Estado del Caso: en Investigacion'. Para el tono de la narrativa, quiero que las emociones predominantes sean: 'labels_genericas': ['calculado', 'organizado', 'desorganizado'], 'labels_motivo_crimen': ['robo con violencia', 'familiar', 'disparo'], 'labels_escena_caracteristicas': ['arma improvisada', 'maletero', 'arma de fuego'], 'labels_contexto_clasificacion': ['violento', 'conocido', 'víctima vulnerable'] Por favor, genera, un relato breve: El Gancho: Un inicio potente con una voz narrativa en primera persona, cargada de cinismo y descripciones sensoriales. Atmósfera: Describe el entorno (la ciudad, el clima, la iluminación) usando las etiquetas sentimentales como filtro."
def generar_historia(data) -> str:
    response: ChatResponse = chat(model='gemma4:e2b', messages=[
  {
    'role': 'user',
    'content': script,
  },
])

    return response.message.content

if __name__ == "__main__":
    print(generar_historia(None))
#     df=pd.read_csv("data\\crimeData_limpio.csv")
# if __name__=="__main__":
#    print(construir_clasificacion(df.iloc[6220],df.iloc[6220]["Status Desc"]))
    # texto = input("Tú: ")
    # resultado = preguntar_a_grok(texto)
    # print(f"Grok: {resultado}")