#!/usr/bin/env bash
set -euo pipefail

if [[ ! -x .venv/bin/uvicorn ]]; then
  echo "No existe uvicorn en .venv. Ejecuta primero scripts/3_instalar_dependencias.sh" >&2
  exit 1
fi

.venv/bin/uvicorn backend.main:app --reload
