"""
Gestión de rutas para Galaxy Runner
Maneja todas las rutas de archivos y ubicaciones de recursos
"""

import os
import sys

# Directorio base - apunta a la carpeta galaxy_runner
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cuando se ejecuta el ejecutable de PyInstaller, los archivos se extraen en
# sys._MEIPASS. Ajustamos BASE_DIR para apuntar a la copia empaquetada.
if hasattr(sys, '_MEIPASS'):
    BASE_DIR = os.path.join(sys._MEIPASS, 'galaxy_runner')

# Directorios de recursos
RES_DIR = os.path.join(BASE_DIR, 'res')
IMG_DIR = os.path.join(RES_DIR, 'img')
SFX_DIR = os.path.join(RES_DIR, 'sfx')
FONTS_DIR = os.path.join(RES_DIR, 'fonts')

# Base de datos - almacenar en el directorio padre de galaxy_runner
DB_NAME = "galaxy_runner.db"
DB_PATH = os.path.join(os.path.dirname(BASE_DIR), DB_NAME)

# Rutas de imágenes
def get_image_path(filename: str) -> str:
    """Obtener ruta completa a un archivo de imagen"""
    return os.path.join(IMG_DIR, filename)

def get_sfx_path(filename: str) -> str:
    """Obtener ruta completa a un archivo de efecto de sonido"""
    return os.path.join(SFX_DIR, filename)

def get_font_path(filename: str) -> str:
    """Obtener ruta completa a un archivo de fuente"""
    return os.path.join(FONTS_DIR, filename)

