import os
import google.generativeai as genai
import time
from pathlib import Path

def setup_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return False
    genai.configure(api_key=api_key)
    return True

def procesar_multimedia(file_path: str, media_type: str = "image") -> str:
    """
    Sube y analiza un archivo (video o imagen) usando Gemini 1.5 Pro.
    Retorna un resumen estructurado.
    """
    if not setup_gemini():
        return "❌ Error: La variable GEMINI_API_KEY no está configurada en el archivo .env."
    
    if not os.path.exists(file_path):
        return "❌ Error: El archivo multimedia no se encontró en el servidor."

    try:
        print(f"Subiendo archivo {file_path} a Gemini API...")
        uploaded_file = genai.upload_file(path=file_path)
        
        if media_type == "video":
            print(f"Archivo subido como {uploaded_file.uri}. Esperando procesamiento de video...")
            while uploaded_file.state.name == "PROCESSING":
                print(".", end="", flush=True)
                time.sleep(5)
                uploaded_file = genai.get_file(uploaded_file.name)
            print()
            if uploaded_file.state.name == "FAILED":
                return "❌ Error: Gemini falló al procesar el video."
        
        prompt = (
            "Eres el Córtex Visual de JARVIS. Analiza detenidamente este material "
            "sobre novedades de inteligencia artificial. Entrégame un resumen ejecutivo "
            "claro, estructurado y al grano con lo más importante (herramientas, impactos, "
            "funcionalidades)."
        )
        
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        print("Solicitando análisis al modelo...")
        response = model.generate_content([uploaded_file, prompt])
        
        try:
            genai.delete_file(uploaded_file.name)
        except:
            pass
            
        return f"👁️ **Análisis Visual (Córtex Gemini 1.5 Pro)**:\n\n{response.text}"
        
    except Exception as e:
        return f"❌ Error en el análisis multimodal: {str(e)}"
