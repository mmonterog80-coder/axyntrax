import os
import requests
import uuid
from pathlib import Path
from openai import OpenAI
from fish_audio_sdk import Session, TTSRequest

# Claves de API
FISH_API_KEY = os.getenv("FISH_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# IDs de Voces Oficiales
FISH_JARVIS_ID = "21adf3cda02a4aa88dc593353cc9d715"
ELEVENLABS_VOICE_ID = "ErXwobaYiN019PkySvjV" 

def generar_audio(texto: str, archivo_salida: str = None) -> str:
    """Genera audio usando la mejor voz disponible (Fish Audio > OpenAI > ElevenLabs)"""
    workspace = Path(os.path.dirname(__file__)) / ".." / ".." / "workspace"
    workspace.mkdir(exist_ok=True)
    
    if not archivo_salida:
        archivo_salida = str(workspace / f"jarvis_respuesta_{uuid.uuid4().hex[:6]}.mp3")
        
    # Preferencia 1: Fish Audio SDK (Voz Oficial Jarvis Latino/México - Configurada por el CEO)
    if FISH_API_KEY:
        try:
            session = Session(apikey=FISH_API_KEY)
            audio = b""
            with session.tts(TTSRequest(
                reference_id=FISH_JARVIS_ID,
                text=texto
            )) as response:
                for chunk in response:
                    audio += chunk
            with open(archivo_salida, "wb") as f:
                f.write(audio)
            return archivo_salida
        except Exception as e:
            print(f"Error Fish Audio: {e}. Intentando fallback...")

    # Preferencia 2: OpenAI TTS (Voz Onyx)
    if OPENAI_API_KEY:
        try:
            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.audio.speech.create(
                model="tts-1",
                voice="onyx",
                input=texto
            )
            response.stream_to_file(archivo_salida)
            return archivo_salida
        except Exception as e:
            print(f"Error OpenAI TTS: {e}. Intentando fallback...")

    # Preferencia 3: ElevenLabs
    if ELEVENLABS_API_KEY:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
        headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
        payload = {"text": texto, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.7, "similarity_boost": 0.5}}
        try:
            r = requests.post(url, json=payload, headers=headers, timeout=10)
            if r.status_code == 200:
                with open(archivo_salida, "wb") as f:
                    f.write(r.content)
                return archivo_salida
            else:
                return f"[Error ElevenLabs: {r.status_code}]"
        except Exception as e:
            return f"[Error: {e}]"
            
    return "[Error: No hay API Keys configuradas para TTS en el archivo .env (FISH_API_KEY requerida)]"

def reproducir_audio(texto: str):
    ruta = generar_audio(texto)
    if ruta and not ruta.startswith("[Error"):
        import subprocess
        subprocess.Popen(["start", ruta], shell=True)
        return True
    return False
