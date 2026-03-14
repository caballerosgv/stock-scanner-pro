from __future__ import annotations

import os

import uvicorn



def _prompt_int(message: str, default: int) -> int:
    while True:
        raw_value = input(f"{message} [{default}]: ").strip()
        if not raw_value:
            return default
        if raw_value.isdigit() and int(raw_value) > 0:
            return int(raw_value)
        print("Por favor ingresa un número entero positivo.")



def _prompt_str(message: str, default: str) -> str:
    raw_value = input(f"{message} [{default}]: ").strip()
    return raw_value or default



def run_interactive_launcher() -> None:
    print("=== Stock Scanner Pro (modo ejecutable) ===")
    host = _prompt_str("Host", "127.0.0.1")
    port = _prompt_int("Puerto", 8000)
    scanner_refresh_seconds = _prompt_int("Refresco automático del escáner (segundos)", 45)
    universe_size = _prompt_int("Cantidad de símbolos a escanear", 1200)

    os.environ["SCANNER_REFRESH_SECONDS"] = str(scanner_refresh_seconds)
    os.environ["SCANNER_UNIVERSE_SIZE"] = str(universe_size)

    print("\nIniciando API...")
    print(f"Dashboard: http://{host}:{port}/dashboard")
    print("Para detener, usa Ctrl+C.\n")

    uvicorn.run("backend.main:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    run_interactive_launcher()
