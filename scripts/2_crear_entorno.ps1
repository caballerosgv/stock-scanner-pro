$ErrorActionPreference = 'Stop'

python -m venv .venv

if (-not (Test-Path '.venv\Scripts\python.exe')) {
    Write-Error 'No se pudo crear el entorno virtual en .venv'
}

Write-Host 'Entorno virtual creado en .venv'
