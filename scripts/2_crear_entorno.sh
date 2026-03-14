#!/usr/bin/env bash
set -euo pipefail

python -m venv .venv

if [[ ! -x .venv/bin/python ]]; then
  echo "No se pudo crear el entorno virtual en .venv" >&2
  exit 1
fi

echo "Entorno virtual creado en .venv"
