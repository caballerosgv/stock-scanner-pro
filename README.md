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

## Cómo ejecutar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn backend.main:app --reload
```

Abrir: `http://127.0.0.1:8000`

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
