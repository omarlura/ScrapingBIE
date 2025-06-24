# sources/eventbrite_scraper.py
# Scrapea eventos públicos de Eventbrite para Colombia

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def get_events():
    eventos = []
    url = "https://www.eventbrite.com/d/colombia--bogota/technology/"

    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # No abre ventana
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)

        time.sleep(5)  # Esperar carga JS

        # Cada evento en div.eds-event-card-content__content
        cards = driver.find_elements(By.CSS_SELECTOR, "div.eds-event-card-content__content")

        for card in cards:
            try:
                title_elem = card.find_element(By.CSS_SELECTOR, "div.eds-is-hidden-accessible")
                date_elem = card.find_element(By.CSS_SELECTOR, "div.card-text--truncated__one")
                link_elem = card.find_element(By.XPATH, "..").get_attribute("href")

                eventos.append({
                    "nombre": title_elem.text.strip(),
                    "fecha": date_elem.text.strip() if date_elem else "Sin fecha",
                    "link": link_elem,
                    "origen": "Eventbrite (Scraper)"
                })
            except Exception as e_card:
                print(f"[WARN] Evento con error parcial: {str(e_card)}")

        print(f"[INFO] Eventbrite (Scraper) → {len(eventos)} eventos encontrados.")

        driver.quit()
    except Exception as e:
        print(f"[ERROR] Error al obtener eventos de Eventbrite (Scraper): {str(e)}")

    return eventos
