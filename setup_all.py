import asyncio
import os
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

PORTALS = [
    {"name": "Bumeran", "url": "https://www.bumeran.com.pe/", "state_file": r"C:\AXYNTRAX\bumeran_state.json"},
    {"name": "Aptitus", "url": "https://aptitus.com/", "state_file": r"C:\AXYNTRAX\aptitus_state.json"},
    {"name": "Indeed Perú", "url": "https://pe.indeed.com/", "state_file": r"C:\AXYNTRAX\indeed_state.json"},
    {"name": "Jobted Perú", "url": "https://pe.jobted.com/", "state_file": r"C:\AXYNTRAX\jobted_state.json"},
    {"name": "Trabajando.pe", "url": "https://www.trabajando.pe/", "state_file": r"C:\AXYNTRAX\trabajando_state.json"}
]

async def main():
    print("Iniciando Modo Captura Masiva de Sesiones...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50, channel="chrome")
        context = await browser.new_context(viewport={"width": 1280, "height": 720})
        page = await context.new_page()
        stealth = Stealth()
        await stealth.apply_stealth_async(page)
        
        for portal in PORTALS:
            print(f"\n========================================================")
            print(f"Navegando a {portal['name']}...")
            await page.goto(portal['url'])
            
            print(f"⚠️ ATENCIÓN: Por favor, regístrate o inicia sesión en {portal['name']}.")
            print(f"Sube tu CV si es necesario.")
            print(f"========================================================\n")
            
            await asyncio.to_thread(input, f"👉 VUELVE A ESTA CONSOLA Y PRESIONA 'ENTER' CUANDO HAYAS TERMINADO CON {portal['name'].upper()}...")
            
            print(f"✅ Guardando llave maestra de {portal['name']}...")
            await context.storage_state(path=portal['state_file'])
            
        print("\n¡Todo listo! Todas las sesiones maestras han sido capturadas con éxito.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
