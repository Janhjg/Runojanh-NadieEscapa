import os
import requests
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = "QtPMrakdgePQIUwOX7Ut" # Detective voice

def generate_voice_narration(text: str):
    """
    Convierte el texto de la crónica en audio usando ElevenLabs.
    """
    if not ELEVENLABS_API_KEY:
        raise ValueError("ELEVENLABS_API_KEY no configurada en el entorno.")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.5,
            "use_speaker_boost": True
        }
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return response.content
    else:
        # Extraer detalle si es posible
        error_msg = response.text
        try:
            error_json = response.json()
            if "detail" in error_json and "message" in error_json["detail"]:
                error_msg = error_json["detail"]["message"]
        except:
            pass
            
        print(f"ELEVENLABS API ERROR [{response.status_code}]: {response.text}")
        raise Exception(f"E11_ERROR: {response.status_code} - {error_msg}")
