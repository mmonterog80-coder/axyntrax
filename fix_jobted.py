import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def main():
    print("Recuperando sesión de Jobted Perú...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50, channel="chrome")
        context = await browser.new_context(viewport={"width": 1280, "height": 720})
        page = await context.new_page()
        stealth = Stealth()
        await stealth.apply_stealth_async(page)
        
        await page.goto("https://pe.jobted.com/")
        print("⚠️ ATENCIÓN: Inicia sesión en Jobted Perú.")
        
        await asyncio.to_thread(input, "👉 VUELVE A ESTA CONSOLA Y PRESIONA 'ENTER' CUANDO HAYAS INICIADO SESIÓN...")
        
        await context.storage_state(path=r"C:\AXYNTRAX\jobted_state.json")
        print("✅ Llave de Jobted guardada con éxito.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
