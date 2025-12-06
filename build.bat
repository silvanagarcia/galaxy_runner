@echo off
setlocal enabledelayedexpansion

REM =============================================================
REM  Galaxy Runner - Build Script
REM  Empaqueta el juego completo usando PyInstaller
REM =============================================================

set PROJECT_ROOT=%~dp0
pushd "%PROJECT_ROOT%"

set DIST_NAME=GalaxyRunner
set DIST_DIR=%PROJECT_ROOT%dist\%DIST_NAME%
set DB_FILE=%PROJECT_ROOT%galaxy_runner.db
set MAIN_FILE=main.py

if not exist "%PROJECT_ROOT%%MAIN_FILE%" (
    echo [ERROR] No se encontro %MAIN_FILE%. Ejecuta este script desde galaxy_runner\.
    goto :EOF
)

REM -- Limpieza previa opcional
if exist dist rd /s /q dist
if exist build rd /s /q build
if exist %DIST_NAME%.spec del %DIST_NAME%.spec

REM -- Ejecutar PyInstaller
py -3 -m PyInstaller ^
    --name "%DIST_NAME%" ^
    --clean ^
    --noconfirm ^
    --onedir ^
    --windowed ^
    --add-data "res;galaxy_runner\\res" ^
    %MAIN_FILE%

if errorlevel 1 (
    echo [ERROR] Fallo la construccion del ejecutable.
    popd
    exit /b 1
)

REM -- Copiar base de datos (o crear una nueva vacia) dentro del paquete
if not exist "%DIST_DIR%" (
    echo [ADVERTENCIA] No se encontro el directorio de salida esperado: %DIST_DIR%
) else (
    if exist "%DB_FILE%" (
        copy /Y "%DB_FILE%" "%DIST_DIR%\galaxy_runner.db" >nul
    ) else (
        type nul > "%DIST_DIR%\galaxy_runner.db"
    )
)

popd
echo [OK] Ejecutable generado en dist\%DIST_NAME%\
exit /b 0
