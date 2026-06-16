import requests
from bs4 import BeautifulSoup
from ddgs import DDGS

def buscar_en_internet(query: str, max_resultados: int = 3):
    """Realiza una búsqueda autónoma usando DuckDuckGo."""
    try:
        ddgs = DDGS()
        resultados = list(ddgs.text(query, max_results=max_resultados))
        return resultados
    except Exception as e:
        print(f"Error en búsqueda: {e}")
        return []

def investigar_competencia(rubro: str):
    """
    Busca de forma inteligente los precios y ofertas de la competencia 
    en un rubro específico. NOVA y JARVIS pueden usar esto para mejorar ofertas.
    """
    query = f"precios de servicios de inteligencia artificial chatbot {rubro} peru o latinoamerica"
    resultados = buscar_en_internet(query)
    
    informe = []
    for res in resultados:
        url = res.get("href")
        title = res.get("title")
        snippet = res.get("body")
        
        informe.append({
            "competidor": title,
            "url": url,
            "resumen_oferta": snippet
        })
        
    return informe

if __name__ == "__main__":
    print("Iniciando escaneo de la red (Fase 4)...")
    reporte = investigar_competencia("bienes raices inmobiliaria")
    for r in reporte:
        print(f"\n[+] Competidor: {r['competidor']}\n[>] Datos: {r['resumen_oferta']}")
