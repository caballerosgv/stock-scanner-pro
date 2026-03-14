$ErrorActionPreference = 'Stop'

if (-not (Test-Path '.venv\Scripts\pip.exe')) {
    Write-Error 'No existe .venv. Ejecuta primero scripts/2_crear_entorno.ps1'
}

& '.venv\Scripts\pip.exe' install -e '.[dev]'
