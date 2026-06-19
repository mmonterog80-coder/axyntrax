import os, logging
logger = logging.getLogger(__name__)

def generar_audio(text, output="response.mp3"):
    key = os.getenv("FISH_API_KEY", "")
    if not key:
        logger.warning("FISH_API_KEY missing. Voice disabled safely.")
        return None
    try:
        from fish_audio_sdk import Session, TTSRequest
        session = Session(key)
        req = TTSRequest(text=str(text)[:500], format="mp3")
        
        audio_chunks = []
        for chunk in session.tts(req):
            audio_chunks.append(chunk)
            
        with open(output, "wb") as f:
            f.write(b"".join(audio_chunks))
        return output
    except Exception as e:
        logger.error(f"Voice generation failed: {e}")
        return None

def generate_voice(text, output="response.mp3"):
    return generar_audio(text, output)

def reproducir_audio(file_path):
    pass