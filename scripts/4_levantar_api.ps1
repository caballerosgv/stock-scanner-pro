$ErrorActionPreference = 'Stop'

if (-not (Test-Path '.venv\Scripts\uvicorn.exe')) {
    Write-Error 'No existe uvicorn en .venv. Ejecuta primero scripts/3_instalar_dependencias.ps1'
}

& '.venv\Scripts\uvicorn.exe' backend.main:app --reload
