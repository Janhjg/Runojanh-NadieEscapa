import os
import sys
from xai_sdk import Client
from xai_sdk.chat import user, system
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("XAI_API_KEY")
if not api_key:
    sys.exit("Error: XAI_API_KEY no está definida. Revisa tu archivo .env")
    
client = Client(api_key=api_key)

script="Actúa como un novelista experto en género noir y hardboiled. Quiero desarrollar una historia basada en el siguiente caso criminal en un limite cercano a 80-120 palabras, te pasaré algunos datos en ingles, traducelo: "Description of Crime:THEFT OF IDENTITY, Nivel:2, Weapon:UNKNOWN WEAPON/OTHER WEAPON , el dia 07/22/2020 12:00:00 AM, a la hora 1200, en Wilshire, distrito:775, in a MULTI-UNIT DWELLING (APARTMENT, DUPLEX, ETC). Información de la victima: edad= 35, sexo=Femenino descendencia=negra, Estado del Caso: en Investigacion". Para el tono de la narrativa, quiero que las emociones predominantes sean: 'labels_genericas': ['calculado', 'organizado', 'desorganizado'], 'labels_motivo_crimen': ['robo con violencia', 'familiar', 'disparo'], 'labels_escena_caracteristicas': ['arma improvisada', 'maletero', 'arma de fuego'], 'labels_contexto_clasificacion': ['violento', 'conocido', 'víctima vulnerable'] Por favor, genera, un relato breve: El Gancho: Un inicio potente con una voz narrativa en primera persona, cargada de cinismo y descripciones sensoriales.Atmósfera: Describe el entorno (la ciudad, el clima, la iluminación) usando las etiquetas sentimentales como filtro."
def generar_historia(data) -> str:
    chat = client.chat.create(
        model="grok-3"
    )
    chat.append(user(script))
    return chat.sample().content

if __name__ == "__main__":
    pass
    # texto = input("Tú: ")
    # resultado = preguntar_a_grok(texto)
    # print(f"Grok: {resultado}")