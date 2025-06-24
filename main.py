import json, os
import importlib
import logging
from notifiers import enviar_telegram
import config

# Configurar log
logging.basicConfig(
    filename='event_tracker.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def log(msg):
    print(msg)
    logging.info(msg)

def guardar_eventos_nuevos(eventos):
    output_file = "data/eventos_guardados.json"
    existentes = []

    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                contenido = f.read().strip()
                if contenido:
                    existentes = json.loads(contenido)
                else:
                    log("[WARN] El archivo eventos_guardados.json está vacío. Se inicializa.")
        except json.JSONDecodeError as e:
            log(f"[ERROR] Error al leer eventos_guardados.json: {str(e)}")
            existentes = []

    existentes_ids = {
        f"{e['nombre'].strip()}|{e['fecha'].strip()}|{e['origen']}" for e in existentes
    }

    nuevos = []
    for e in eventos:
        event_id = f"{e['nombre'].strip()}|{e['fecha'].strip()}|{e['origen']}"
        if event_id not in existentes_ids:
            nuevos.append(e)
            existentes_ids.add(event_id)

    if nuevos:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(existentes + nuevos, f, indent=2, ensure_ascii=False)
        log(f"[INFO] Guardados {len(nuevos)} nuevos eventos.")
    else:
        log("[INFO] No hay eventos nuevos.")

    return nuevos

if __name__ == "__main__":
    log("=== INICIO DE RECOLECCIÓN DE EVENTOS DINÁMICA ===")
    eventos = []

    # Leer fuentes activas desde config_fuentes.json
    with open("config_fuentes.json", "r") as f:
        config_fuentes = json.load(f)

    fuentes_activas = config_fuentes.get("fuentes_activas", [])

    # Cargar dinámicamente cada fuente
    for fuente in fuentes_activas:
        try:
            modulo = importlib.import_module(f"sources.{fuente}")
            eventos_fuente = modulo.get_events()
            log(f"[INFO] {fuente}: {len(eventos_fuente)} eventos.")
            eventos += eventos_fuente
        except Exception as e:
            log(f"[ERROR] No se pudo procesar fuente {fuente}: {str(e)}")

    log("=== VERIFICANDO NUEVOS EVENTOS ===")
    nuevos = guardar_eventos_nuevos(eventos)
    log(f"[INFO] Nuevos eventos agregados: {len(nuevos)}")

    if nuevos:
        log("[INFO] Enviando notificaciones por Telegram...")
        enviar_telegram(nuevos)
    else:
        log("[INFO] No hay eventos nuevos para notificar.")