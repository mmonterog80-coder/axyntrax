import browser_cookie3
import json
import time

def extract_cookies_for_domain(domain, output_file):
    print(f"Buscando cookies para {domain} en Chrome...")
    try:
        cj = browser_cookie3.chrome(domain_name=domain)
    except Exception as e:
        print(f"Error extrayendo cookies de Chrome para {domain}: {e}")
        return

    playwright_cookies = []
    for cookie in cj:
        cookie_dict = {
            "name": cookie.name,
            "value": cookie.value,
            "domain": cookie.domain,
            "path": cookie.path,
            "expires": cookie.expires if cookie.expires else (time.time() + 31536000),
            "httpOnly": cookie.has_nonstandard_attr('HttpOnly'),
            "secure": cookie.secure,
            "sameSite": "Lax"
        }
        playwright_cookies.append(cookie_dict)

    if not playwright_cookies:
        print(f"No se encontraron cookies de {domain} en Chrome.")
        return
        
    state = {
        "cookies": playwright_cookies,
        "origins": []
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4)
        
    print(f"¡Extracción exitosa! {len(playwright_cookies)} cookies de {domain} guardadas en {output_file}")

def main():
    extract_cookies_for_domain("computrabajo.com", r"C:\AXYNTRAX\computrabajo_state.json")
    extract_cookies_for_domain("linkedin.com", r"C:\AXYNTRAX\linkedin_state.json")

if __name__ == "__main__":
    main()
