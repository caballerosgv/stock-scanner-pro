#!/usr/bin/env bash
set -euo pipefail

if [[ ! -x .venv/bin/pip ]]; then
  echo "No existe .venv. Ejecuta primero scripts/2_crear_entorno.sh" >&2
  exit 1
fi

.venv/bin/pip install -e .[dev]
