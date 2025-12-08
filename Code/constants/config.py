

import os
import sys

# ============================================================================
# RUTAS Y DIRECTORIOS
# ============================================================================

# Directorio base - apunta a la carpeta Code
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Cuando se ejecuta el ejecutable de PyInstaller, los archivos se extraen en
# sys._MEIPASS. Ajustamos BASE_DIR para apuntar a la copia empaquetada.
if hasattr(sys, '_MEIPASS'):
    BASE_DIR = os.path.join(sys._MEIPASS, 'Code')

# Directorios de recursos
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
IMG_DIR = os.path.join(ASSETS_DIR, 'images')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')
MUSIC_DIR = os.path.join(SOUNDS_DIR, 'music')
SFX_DIR = os.path.join(SOUNDS_DIR, 'sfx')
BACKGROUNDS_DIR = os.path.join(ASSETS_DIR, 'backgrounds')
FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')

# Base de datos - almacenar en el directorio db
DB_NAME = "galaxy.db"
DB_PATH = os.path.join(BASE_DIR, 'db', DB_NAME)

# ============================================================================
# FUNCIONES DE AYUDA PARA RUTAS
# ============================================================================

def get_image_path(filename: str) -> str:
    
    return os.path.join(IMG_DIR, filename)

def get_music_path(filename: str) -> str:
    
    return os.path.join(MUSIC_DIR, filename)

def get_sfx_path(filename: str) -> str:
    
    return os.path.join(SFX_DIR, filename)

def get_background_path(filename: str) -> str:
    
    return os.path.join(BACKGROUNDS_DIR, filename)

def get_font_path(filename: str) -> str:
    
    return os.path.join(FONTS_DIR, filename)

# ============================================================================
# CONFIGURACIÓN DE PANTALLA
# ============================================================================

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# ============================================================================
# COLORES
# ============================================================================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)

# ============================================================================
# CONFIGURACIÓN DEL JUEGO
# ============================================================================

# Velocidades
PLAYER_SPEED = 500
ENEMY_SPEED_BASE = 300
PROJECTILE_SPEED = 600
METEOR_SPEED_BASE = 300

# Jugador
PLAYER_LIVES = 3

# Enemigos y meteoritos
MAX_ENEMIES_ON_SCREEN = 10
METEOR_SPAWN_INTERVAL = 6

# ============================================================================
# SISTEMA DE PUNTUACIÓN
# ============================================================================

POINTS_ENEMY = 20
POINTS_METEOR = 50
POINTS_BOSS_1 = 100
POINTS_BOSS_2 = 200
POINTS_BOSS_3 = 300

MAX_TOP_SCORES = 10
