@echo off
setlocal

REM =============================================================
REM  Galaxy Runner - Build (Windows)
REM  Genera el ejecutable con PyInstaller a partir del .spec.
REM  Ejecutar desde la RAIZ del repositorio:  build\build.bat
REM =============================================================

REM -- Ubicarse en la raiz del repo (carpeta padre de este script)
pushd "%~dp0.."

if not exist "src\main.py" (
    echo [ERROR] No se encontro src\main.py. Ejecuta este script desde la raiz del repo.
    popd
    exit /b 1
)

REM -- Limpieza previa
if exist build\build rd /s /q build\build
if exist build\dist  rd /s /q build\dist

py -3 -m PyInstaller build\GalaxyRunner.spec ^
    --clean ^
    --noconfirm ^
    --distpath build\dist ^
    --workpath build\build

if errorlevel 1 (
    echo [ERROR] Fallo la construccion del ejecutable.
    popd
    exit /b 1
)

echo [OK] Ejecutable generado en build\dist\
popd
exit /b 0
