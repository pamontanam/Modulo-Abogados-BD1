@echo off
REM ========================================================================
REM Script para Iniciar - Sistema de Gestión de Casos y Expedientes
REM Windows PowerShell
REM ========================================================================

setlocal enabledelayedexpansion

echo.
echo ╔═════════════════════════════════════════════════════════════════╗
echo ║  Sistema de Gestión de Casos y Expedientes - Gabinete Abogados ║
echo ║                         Iniciando...                            ║
echo ╚═════════════════════════════════════════════════════════════════╝
echo.

REM Obtener ruta del script
set SCRIPT_DIR=%~dp0

REM Verificar que exista la estructura de carpetas
if not exist "%SCRIPT_DIR%src\backend" (
    echo [ERROR] Carpeta src\backend no encontrada
    pause
    exit /b 1
)

if not exist "%SCRIPT_DIR%src\frontend" (
    echo [ERROR] Carpeta src\frontend no encontrada
    pause
    exit /b 1
)

echo [*] Ruta del proyecto: %SCRIPT_DIR%
echo.

REM Verificar Python
echo [*] Verificando Python...
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no está instalado o no está en el PATH
    pause
    exit /b 1
)
echo [OK] Python detectado
echo.

REM Verificar entorno virtual backend
echo [*] Verificando entorno virtual...
if not exist "%SCRIPT_DIR%src\backend\venv" (
    echo [*] Creando entorno virtual...
    cd /d "%SCRIPT_DIR%src\backend"
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
    echo [OK] Entorno virtual creado
    echo.
    
    REM Instalar dependencias
    echo [*] Instalando dependencias...
    call venv\Scripts\activate.bat
    pip install --upgrade pip > nul 2>&1
    pip install -r requirements.txt > nul 2>&1
    if errorlevel 1 (
        echo [ERROR] No se pudieron instalar las dependencias
        pause
        exit /b 1
    )
    echo [OK] Dependencias instaladas
    echo.
)

echo [*] Iniciando servicios...
echo.

REM Abrir Terminal 1 para Backend
start "Backend - FastAPI" cmd /k "cd /d %SCRIPT_DIR%src\backend && call venv\Scripts\activate.bat && python main.py"

REM Esperar a que Backend inicie
echo [*] Backend iniciando en puerto 8000...
timeout /t 3 /nobreak

REM Abrir Terminal 2 para Frontend
start "Frontend - HTTP Server" cmd /k "cd /d %SCRIPT_DIR%src\frontend && python -m http.server 8001"

echo [*] Frontend iniciando en puerto 8001...
echo.
echo ╔═════════════════════════════════════════════════════════════════╗
echo ║                    ¡SISTEMA INICIADO!                          ║
echo ╠═════════════════════════════════════════════════════════════════╣
echo ║                                                                 ║
echo ║  [OK] Backend (API):       http://localhost:8000               ║
echo ║  [OK] Frontend (Web):      http://localhost:8001               ║
echo ║  [OK] Documentación API:   http://localhost:8000/docs          ║
echo ║  [OK] Health Check:        http://localhost:8000/api/health    ║
echo ║                                                                 ║
echo ║  Espere a que se cargue la página en el navegador...          ║
echo ║                                                                 ║
echo ║  Para detener: Cierre las ventanas o presione Ctrl+C           ║
echo ║                                                                 ║
echo ╚═════════════════════════════════════════════════════════════════╝
echo.

REM Esperar a que el usuario cierre
timeout /t 5 /nobreak

REM Abrir navegador automáticamente (opcional)
start http://localhost:8001

pause
