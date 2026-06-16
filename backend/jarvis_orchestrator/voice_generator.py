import os, logging
from fish_audio_sdk import FishAudioClient, TTSRequest, AudioFormat
logger = logging.getLogger(__name__)
def generate_voice(text, output="response.mp3"):
    key = os.getenv("FISH_API_KEY")
    if not key:
        logger.warning("FISH_API_KEY not set")
        return None
    try:
        client = FishAudioClient(key)
        req = TTSRequest(text=text, voice_id="jarvis", audio_format=AudioFormat.MP3)
        resp = client.synthesize(req)
        with open(output, "wb") as f:
            f.write(resp.audio)
        logger.info("Voice generated")
        return output
    except Exception as e:
        logger.error(f"Voice error: {e}")
        return None

def generar_audio(text, output="response.mp3"):
    return generate_voice(text, output)

def reproducir_audio(audio_file):
    if audio_file and os.path.exists(audio_file):
        pass