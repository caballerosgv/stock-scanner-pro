# Stock Scanner Pro

Aplicación profesional de stock scanning inspirada en TradingView Screener.

## Stack
- **Backend:** Python + FastAPI + SQLAlchemy async
- **Motor de escaneo:** asíncrono, paralelo, con caché
- **Indicadores:** RSI, SMA20/50/200, Volumen relativo, ATR, MACD
- **Frontend:** dashboard web moderno con tabla interactiva y filtros
- **Base de datos:** SQLite (lista para migrar a PostgreSQL)
- **Alertas:** Telegram, email y notificaciones web (adaptadores iniciales)

## Estructura

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
```

## Fases implementadas

### FASE 1 — Motor de escaneo funcional ✅
- Escaneo de universo >= 1000 símbolos (configurable, default 1200).
- Procesamiento paralelo con `asyncio`.
- Cálculo técnico completo y scoring 0–10.

### FASE 2 — Dashboard web ✅
- Tabla interactiva con ordenación por columnas.
- Filtros dinámicos de score y exchange.
- Botón de escaneo manual y refresco automático cada 45s.

### FASE 3 — Alertas ✅ (base preparada)
- Dispatcher de alertas para Telegram, email y web notifications.
- Disparo automático en oportunidades de score alto.

### FASE 4 — Optimización y escalado ✅ (primera iteración)
- Caché de mercado (TTL 30s) + caché de resultados de escaneo.
- Logging estructurado + manejo básico de errores.
- Tests base para scoring, engine y API.

## Guía paso a paso para hacerlo funcionar

### 1) Verificar prerrequisitos
Antes de empezar, asegúrate de tener:

- Python 3.11+ instalado.
- `pip` disponible.
- Un navegador web moderno (Chrome, Firefox, Edge).

Comando sugerido para verificar Python:

```bash
python --version
```

### 2) Clonar el repositorio

```bash
git clone <URL_DEL_REPO>
cd stock-scanner-pro
```

> Si ya tienes el proyecto descargado, solo entra a la carpeta raíz.

### 3) Crear y activar entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate
```

En Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 4) Instalar dependencias

```bash
pip install -e .[dev]
```

Esto instala backend, librerías de desarrollo y tests.

### 5) Levantar la API

```bash
uvicorn backend.main:app --reload
```

Si todo está bien, verás logs de FastAPI/Uvicorn indicando que el servidor está corriendo.

### 6) Abrir la aplicación en el navegador

- API base: `http://127.0.0.1:8000`
- Healthcheck: `http://127.0.0.1:8000/health`
- Dashboard: `http://127.0.0.1:8000/dashboard`

### 7) Probar un escaneo rápido
Puedes lanzar un escaneo desde el dashboard o por API:

```bash
curl -X POST http://127.0.0.1:8000/api/scan
```

Luego consultar resultados:

```bash
curl http://127.0.0.1:8000/api/results
```

### 8) (Opcional) Ejecutar tests

```bash
pytest
```


## Atajos con archivos ejecutables (1, 2, 3, 4)

Si prefieres ejecutar el setup con scripts numerados en Linux/macOS, usa:

```bash
./scripts/1_verificar_prerrequisitos.sh
./scripts/2_crear_entorno.sh
./scripts/3_instalar_dependencias.sh
./scripts/4_levantar_api.sh
```

En Windows con PowerShell, usa:

```powershell
.\scripts\1_verificar_prerrequisitos.ps1
.\scripts\2_crear_entorno.ps1
.\scripts\3_instalar_dependencias.ps1
.\scripts\4_levantar_api.ps1
```

> Nota: el script 4 deja corriendo Uvicorn en primer plano.


## Generar un `.exe` que pida datos en consola (Windows)

Sí, se puede. Incluimos un launcher interactivo en `backend/exe_launcher.py` que te pide:
- host
- puerto
- segundos de refresco
- tamaño de universo

Luego arranca la API automáticamente con esos valores.

### Pasos rápidos

1. Activa tu entorno virtual e instala dependencias:

```powershell
pip install -e .
pip install pyinstaller
```

2. Genera el ejecutable:

```powershell
pyinstaller --onefile --name stock-scanner-launcher backend/exe_launcher.py
```

3. Ejecuta el `.exe` generado:

```powershell
.\dist\stock-scanner-launcher.exe
```

4. Abre el dashboard en la URL que te muestre la consola (por defecto `http://127.0.0.1:8000/dashboard`).

## Empaquetar en un instalador `setup.exe` (Windows)

Sí, también se puede empaquetar como instalador clásico `setup.exe`.

La idea es:
- construir primero `stock-scanner-launcher.exe` con PyInstaller,
- incluir ese `.exe` dentro de un instalador (por ejemplo, con Inno Setup),
- crear accesos directos para que el usuario final lo abra sin usar terminal.

### 1) Generar el ejecutable base

```powershell
pip install -e .
pip install pyinstaller
pyinstaller --onefile --name stock-scanner-launcher backend/exe_launcher.py
```

### 2) Crear `setup.exe` con Inno Setup

1. Instala Inno Setup.
2. Crea un archivo `installer/stock-scanner-pro.iss` con este contenido:

```iss
[Setup]
AppName=Stock Scanner Pro
AppVersion=0.1.0
DefaultDirName={autopf}\Stock Scanner Pro
DefaultGroupName=Stock Scanner Pro
OutputDir=dist
OutputBaseFilename=stock-scanner-setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\stock-scanner-launcher.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Stock Scanner Pro"; Filename: "{app}\stock-scanner-launcher.exe"
Name: "{autodesktop}\Stock Scanner Pro"; Filename: "{app}\stock-scanner-launcher.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Accesos directos:"; Flags: unchecked
```

3. Compila el script desde Inno Setup Compiler.
4. El instalador final quedará en `dist/stock-scanner-setup.exe`.

Con esto, sí tendrás una experiencia “instalar y abrir” para la app web local.

## Problemas comunes

- **`ModuleNotFoundError` al iniciar**: verifica que el entorno virtual esté activo y vuelve a ejecutar `pip install -e .[dev]`.
- **Puerto en uso (`8000`)**: arranca en otro puerto, por ejemplo:
  ```bash
  uvicorn backend.main:app --reload --port 8001
  ```
- **No carga el dashboard**: confirma que estés usando la ruta `http://127.0.0.1:8000/dashboard` y no solo la raíz.

## Endpoints
- `GET /health`
- `POST /api/scan` Ejecuta escaneo completo.
- `GET /api/results` Últimos resultados persistidos.
- `GET /api/provider-configs` Estado de configuración de APIs por proveedor.
- `PUT /api/provider-configs/{provider}` Guarda o actualiza la API key de un proveedor.

## Notas de producción
- Cambiar `DATABASE_URL` a PostgreSQL para entorno real.
- Reemplazar `SyntheticMarketDataProvider` por proveedor market-data real (Polygon, IEX, Alpaca, etc).
- Integrar cola de background workers (Celery/RQ) para horizontal scaling.
