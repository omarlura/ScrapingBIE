# validador_fuentes.py
# Valida que todas las fuentes activas estén bien implementadas.

import importlib
import json

# Requisitos por evento
claves_requeridas = ["nombre", "fecha", "link", "origen"]

# Leer fuentes activas
with open("config_fuentes.json", "r") as f:
    config_fuentes = json.load(f)

fuentes_activas = config_fuentes.get("fuentes_activas", [])

print("=== VALIDACIÓN DE FUENTES ACTIVAS ===")
errores = 0

for fuente in fuentes_activas:
    print(f"\nValidando fuente: {fuente}")

    try:
        modulo = importlib.import_module(f"sources.{fuente}")

        if not hasattr(modulo, "get_events"):
            print(f"[ERROR] La fuente '{fuente}' NO tiene función 'get_events()'.")
            errores += 1
            continue

        eventos = modulo.get_events()

        if not isinstance(eventos, list):
            print(f"[ERROR] La fuente '{fuente}' NO retorna una lista.")
            errores += 1
            continue

        for idx, evento in enumerate(eventos):
            if not isinstance(evento, dict):
                print(f"[ERROR] Fuente '{fuente}', evento #{idx+1} NO es un dict.")
                errores += 1
                break

            for clave in claves_requeridas:
                if clave not in evento:
                    print(f"[ERROR] Fuente '{fuente}', evento #{idx+1} le falta clave '{clave}'.")
                    errores += 1

        print(f"[OK] Fuente '{fuente}' validada correctamente. Eventos: {len(eventos)}.")

    except Exception as e:
        print(f"[ERROR] Fallo al procesar fuente '{fuente}': {str(e)}")
        errores += 1

print("\n=== VALIDACIÓN COMPLETADA ===")

if errores == 0:
    print("[RESULTADO] ✅ Todas las fuentes están correctamente implementadas.")
else:
    print(f"[RESULTADO] ❌ Se encontraron {errores} errores en la validación.")
