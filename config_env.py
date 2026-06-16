import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el .env principal (Vault)
load_dotenv(r"C:\AXYNTRAX\.env")

# --- Credenciales de Usuario y Contacto ---
MIGUEL_EMAIL = os.getenv("MIGUEL_EMAIL", "miguel.montero@example.com")
MIGUEL_TELEFONO = os.getenv("MIGUEL_TELEFONO", "+51 900 000 000")
MIGUEL_LINKEDIN_URL = os.getenv("MIGUEL_LINKEDIN_URL", "https://linkedin.com/in/miguelmontero")

# --- DeepSeek ---
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")

# --- Supabase ---
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# --- Mensajería (JARVIS / WhatsApp) ---
WHATSAPP_API_KEY = os.getenv("WHATSAPP_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# --- Fish Audio (JARVIS Voice) ---
FISH_AUDIO_KEY = os.getenv("FISH_AUDIO_KEY", "")
JARVIS_VOICE_ID = os.getenv("JARVIS_VOICE_ID", "21adf3cda02a4aa88dc593353cc9d715")

# --- Rutas Locales ---
CV_PATH = os.getenv("CV_PATH", r"C:\Users\YARVIS\Desktop\certificados\CV_MIGUEL_MONTERO_LITE.pdf")
CV_TEXT_PATH = os.getenv("CV_TEXT_PATH", r"C:\AXYNTRAX\cv_text.txt")
LOCAL_DB_PATH = r"C:\AXYNTRAX\postulaciones.db"
