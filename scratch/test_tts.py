from services.tts_service import generate_voice_narration
import os
from dotenv import load_dotenv

load_dotenv()

try:
    print("Testing ElevenLabs TTS...")
    result = generate_voice_narration("Prueba de audio para el sistema Runojanh.")
    print(f"Success! Received {len(result)} bytes of audio.")
except Exception as e:
    print(f"Error: {e}")
