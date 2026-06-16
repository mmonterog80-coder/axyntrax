import os
import time
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv(dotenv_path="C:\\AXYNTRAX\\backend\\worker\\.env")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def fetch_hacker_news_top_stories(limit=30):
    """Obtiene las historias top de Hacker News"""
    try:
        log("Consultando Hacker News API...")
        # Obtener los IDs de las mejores historias
        r = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")
        if r.status_code != 200:
            log("Error al conectar con Hacker News.")
            return []
            
        story_ids = r.json()[:limit]
        stories = []
        
        log(f"Analizando {len(story_ids)} historias principales...")
        for sid in story_ids:
            sr = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json")
            if sr.status_code == 200:
                item = sr.json()
                if item and "title" in item:
                    stories.append(item["title"])
        return stories
    except Exception as e:
        log(f"Fallo en scraping de Hacker News: {e}")
        return []

def filter_tech_trends(stories):
    """Filtra las historias buscando keywords de la industria"""
    keywords = ["ai", "llm", "agent", "automation", "b2b", "saas", "api", "bot", "rag", "deepseek", "openai"]
    relevant = []
    for s in stories:
        title_lower = s.lower()
        if any(kw in title_lower for kw in keywords):
            relevant.append(s)
    return relevant

def generate_architect_mission(trends):
    """Usa DeepSeek para transformar tendencias en una Misión para AXYNTRAX"""
    if not DEEPSEEK_API_KEY:
        log("ERROR: Falta DEEPSEEK_API_KEY. No se puede generar misión.")
        return None
        
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = (
        "Eres JARVIS, el analista de mercado de AXYNTRAX Corp. "
        "Has detectado las siguientes tendencias en el mercado tecnológico de hoy:\n"
        f"{chr(10).join(trends)}\n\n"
        "Tu objetivo es elegir LA MEJOR TENDENCIA y redactar una misión directa, "
        "técnica y accionable para el Arquitecto Autónomo. La misión debe ordenarle "
        "al arquitecto construir un nuevo módulo web, componente en Next.js, script en python "
        "o base de datos para AXYNTRAX basado en esa tendencia.\n"
        "Sé ultra conciso (máximo 3 líneas). No incluyas saludos. Empieza directamente con la misión."
    )
    
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 200
    }
    
    try:
        log("Consultando al cerebro analítico (DeepSeek)...")
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"].strip()
        else:
            log(f"Error DeepSeek: {r.text}")
    except Exception as e:
        log(f"Fallo conexión con DeepSeek: {e}")
    return None

def main():
    log("========================================")
    log("JARVIS MARKET SCANNER (FASE 1) INICIADO")
    log("========================================")
    
    stories = fetch_hacker_news_top_stories(30)
    if not stories:
        log("No se encontraron historias. Abortando.")
        return
        
    trends = filter_tech_trends(stories)
    if not trends:
        log("No se detectaron tendencias clave de IA/B2B hoy. Usando historias generales.")
        trends = stories[:5]
        
    log(f"Tendencias detectadas: {len(trends)} noticias relevantes.")
    
    mision_text = generate_architect_mission(trends)
    if mision_text:
        log("Misión generada con éxito:")
        print(f"\n{mision_text}\n")
        
        mision_path = "C:\\AXYNTRAX\\backend\\worker\\mision.txt"
        with open(mision_path, "w", encoding="utf-8") as f:
            f.write(mision_text)
        log(f"¡Combustible inyectado en {mision_path}!")
        log("El Arquitecto Autónomo la ejecutará en su próximo ciclo.")
    else:
        log("Fallo al generar la misión.")

if __name__ == "__main__":
    main()
