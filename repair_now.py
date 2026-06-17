import os, subprocess

# 1. Reparar voice_generator.py (versión blindada)
voice_path = r"backend\jarvis_orchestrator\voice_generator.py"
os.makedirs(os.path.dirname(voice_path), exist_ok=True)
with open(voice_path, 'w', encoding='utf-8') as f:
    f.write('''import os, logging
from fish_audio_sdk import FishAudioClient, TTSRequest, AudioFormat
logger = logging.getLogger(__name__)
def generate_voice(text, output="response.mp3"):
    key = os.getenv("FISH_API_KEY")
    if not key:
        logger.warning("FISH_API_KEY no configurada"); return None
    try:
        client = FishAudioClient(key)
        req = TTSRequest(text=text, voice_id="jarvis", audio_format=AudioFormat.MP3)
        resp = client.synthesize(req)
        with open(output, "wb") as f: f.write(resp.audio)
        logger.info("Voz generada"); return output
    except Exception as e:
        logger.error(f"Fallo voz: {e}"); return None
''')
print("voice_generator.py reparado.")

# 2. Limpiar staging de Git y subir CHAU CHAMBA
os.chdir(r"C:\AXYNTRAX")
subprocess.run(["git", "reset", "HEAD", "."], shell=True)
with open(".gitignore", "a") as gf:
    gf.write("\nbackend/venv/\n")
subprocess.run(["git", "add", "-A"], shell=True)
subprocess.run(["git", "commit", "-m", "CHAU CHAMBA cloud-ready (auto-push)"], shell=True)
result = subprocess.run(["git", "push", "origin", "master"], shell=True, capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
print("Push completado. Railway desplegará CHAU CHAMBA.")

# 3. Reiniciar JARVIS
subprocess.Popen([r"C:\AXYNTRAX\start_jarvis.bat"], shell=True)
print("JARVIS reiniciado.")
