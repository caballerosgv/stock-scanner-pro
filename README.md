# Stock Scanner Pro

Guía actualizada del proyecto para instalación, ejecución y uso.

## Resumen
Stock Scanner Pro es una aplicación de escaneo de acciones con API FastAPI, almacenamiento en SQLite y un dashboard web servido por la misma API.

## Tecnologías
- Python 3.11+
- FastAPI + Uvicorn
- SQLAlchemy async + aiosqlite
- Frontend estático (HTML/CSS/JS) servido desde FastAPI

## Estructura del proyecto
```txt
backend/
  api/
  scanner/
  indicators/
  alerts/
  database/
frontend/
  dashboard/
  components/
scripts/
```

## Requisitos
- Python 3.11 o superior
- pip

## Instalación rápida
### Linux/macOS
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

### Windows (PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .[dev]
```

## Ejecutar la aplicación
```bash
uvicorn backend.main:app --reload
```

Endpoints principales:
- API base: `http://127.0.0.1:8000`
- Healthcheck: `http://127.0.0.1:8000/health`
- Dashboard: `http://127.0.0.1:8000/`

## Uso básico de la API
Disparar escaneo:
```bash
curl -X POST http://127.0.0.1:8000/api/scan
```

Ver últimos resultados:
```bash
curl http://127.0.0.1:8000/api/results
```

Gestionar proveedores:
- `GET /api/provider-configs`
- `PUT /api/provider-configs/{provider}`

Proveedores soportados:
- polygon
- iex
- alpaca
- finnhub
- twelvedata
- xtb

Configuración opcional para XTB (lectura desde SQLite):
```bash
export XTB_DATABASE_PATH=/ruta/a/xtb.db
export XTB_TABLE_NAME=xtb_ohlcv
```
La tabla esperada debe contener al menos: `symbol`, `timestamp`, `open`, `high`, `low`, `close`, `volume`.

## Scripts de apoyo
Se incluyen scripts numerados para setup y ejecución en `scripts/`:

Linux/macOS:
- `scripts/1_verificar_prerrequisitos.sh`
- `scripts/2_crear_entorno.sh`
- `scripts/3_instalar_dependencias.sh`
- `scripts/4_levantar_api.sh`

Windows (PowerShell):
- `scripts/1_verificar_prerrequisitos.ps1`
- `scripts/2_crear_entorno.ps1`
- `scripts/3_instalar_dependencias.ps1`
- `scripts/4_levantar_api.ps1`

## Tests
```bash
pytest
```
