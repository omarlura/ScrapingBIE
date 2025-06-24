# sources/microsoft_events.py
# Scraper con Selenium para Microsoft Events LATAM

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def get_events():
    eventos = []
    url = "https://www.microsoft.com/es-xl/events/"

    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # No abre ventana
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)

        time.sleep(5)  # Esperar carga JS completa

        # Cada evento es un card → div.event-card_container
        cards = driver.find_elements(By.CSS_SELECTOR, "div.event-card_container")

        for card in cards:
            try:
                title_elem = card.find_element(By.CSS_SELECTOR, "h3")
                date_elem = card.find_element(By.CSS_SELECTOR, "span.event-date")
                link_elem = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

                eventos.append({
                    "nombre": title_elem.text.strip(),
                    "fecha": date_elem.text.strip() if date_elem else "Sin fecha",
                    "link": link_elem,
                    "origen": "Microsoft Events"
                })
            except Exception as e_card:
                print(f"[WARN] Evento con error parcial: {str(e_card)}")

        print(f"[INFO] Microsoft Events (Selenium) → {len(eventos)} eventos encontrados.")

        driver.quit()
    except Exception as e:
        print(f"[ERROR] Error al obtener eventos de Microsoft Events (Selenium): {str(e)}")

    return eventos
