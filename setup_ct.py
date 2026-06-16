import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

STATE_FILE = r"C:\AXYNTRAX\computrabajo_state.json"

async def main():
    print("Iniciando Motor Playwright (Modo Visible)...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50, channel="chrome")
        context = await browser.new_context(viewport={"width": 1280, "height": 720})
        page = await context.new_page()
        stealth = Stealth()
        await stealth.apply_stealth_async(page)
        
        print("\nNavegando a Computrabajo Perú...")
        await page.goto("https://pe.computrabajo.com/")
        
        print("\n========================================================")
        print("⚠️ ATENCIÓN: Inicia sesión en Computrabajo en la ventana.")
        print("========================================================\n")
        
        await asyncio.to_thread(input, "👉 VUELVE A ESTA CONSOLA Y PRESIONA 'ENTER' SOLO CUANDO HAYAS INICIADO SESIÓN...")
        
        print("✅ Guardando sesión maestra...")
        await context.storage_state(path=STATE_FILE)
        print("¡Listo! Sesión de Computrabajo guardada con éxito.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
