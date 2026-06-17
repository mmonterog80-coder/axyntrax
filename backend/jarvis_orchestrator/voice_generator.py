import os, logging
logger = logging.getLogger(__name__)

def generar_audio(text, output="response.mp3"):
    key = os.getenv("FISH_API_KEY", "")
    if not key:
        logger.warning("FISH_API_KEY missing. Voice disabled safely.")
        return None
    try:
        from fish_audio_sdk import FishAudioClient, TTSRequest, AudioFormat
        client = FishAudioClient(key)
        req = TTSRequest(text=str(text)[:500], audio_format=AudioFormat.MP3)
        resp = client.synthesize(req)
        with open(output, "wb") as f:
            f.write(resp.audio)
        return output
    except Exception as e:
        logger.error(f"Voice generation failed: {e}")
        return None

def generate_voice(text, output="response.mp3"):
    return generar_audio(text, output)

def reproducir_audio(file_path):
    pass