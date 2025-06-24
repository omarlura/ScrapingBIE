# sources/keyword_search.py
import requests
from bs4 import BeautifulSoup

def buscar_eventos_por_palabra_clave(palabra_clave):
    url = f"https://www.eventbrite.com/d/online/{palabra_clave}/"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        eventos = []

        for card in soup.select("div.eds-event-card-content__content"):  # CSS selector Eventbrite
            nombre = card.select_one("div.eds-event-card-content__primary-content").get_text(strip=True)
            link = card.find("a", href=True)["href"]
            fecha = card.select_one("div.eds-text-bs--fixed").get_text(strip=True)

            eventos.append({
                "nombre": nombre,
                "fecha": fecha,
                "link": link,
                "origen": f"Web: {palabra_clave}"
            })

        return eventos

    except Exception as e:
        print(f"[ERROR] Fallo al buscar eventos por '{palabra_clave}': {e}")
        return []
