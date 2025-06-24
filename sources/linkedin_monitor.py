# sources/linkedin_monitor.py
# Scraper con Playwright para páginas públicas de LinkedIn (eventos, posts con keywords)

from playwright.sync_api import sync_playwright
import re
import time

def get_events():
    eventos = []

    # Ejemplo: página pública de LinkedIn
    urls = [
        "https://www.linkedin.com/company/isaca-colombia/posts/",
        "https://www.linkedin.com/company/felaban/posts/",
        "https://www.linkedin.com/company/business-agility-latam/posts/",
        "https://www.linkedin.com/"
        
        # Puedes agregar más páginas públicas aquí
    ]

    keywords = re.compile(r"\b(evento|congreso|summit|conferencia|workshop|bootcamp|meetup)\b", re.IGNORECASE)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for url in urls:
                print(f"[INFO] Explorando LinkedIn → {url}")

                page.goto(url)
                time.sleep(5)  # Esperar carga completa

                # Los posts en LinkedIn suelen estar en span.break-words o div.feed-shared-update-v2
                posts = page.locator("span.break-words").all_text_contents()

                for texto in posts:
                    if keywords.search(texto):
                        eventos.append({
                            "nombre": texto.strip()[:100] + "...",
                            "fecha": "Sin fecha (LinkedIn post)",
                            "link": url,
                            "origen": "LinkedIn Monitor"
                        })

                print(f"[INFO] LinkedIn → {len(eventos)} posibles eventos detectados en {url}")

            browser.close()
    except Exception as e:
        print(f"[ERROR] Error al obtener eventos de LinkedIn (Playwright): {str(e)}")

    return eventos