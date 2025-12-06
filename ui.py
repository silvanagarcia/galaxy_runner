"""
Componentes y utilidades de UI para Galaxy Runner
"""

import pygame
from galaxy_runner.paths import IMG_DIR, FONTS_DIR
import os

# Dimensiones de pantalla
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Colores
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

# Configuración del juego
PLAYER_SPEED = 500
ENEMY_SPEED_BASE = 300
PROJECTILE_SPEED = 600
METEOR_SPEED_BASE = 300

PLAYER_LIVES = 3
MAX_ENEMIES_ON_SCREEN = 10
METEOR_SPAWN_INTERVAL = 6

# Sistema de puntuación
POINTS_ENEMY = 20
POINTS_METEOR = 50
POINTS_BOSS_1 = 100
POINTS_BOSS_2 = 200
POINTS_BOSS_3 = 300

MAX_TOP_SCORES = 10

def load_font(size: int, font_name: str = None):
    """Cargar un archivo de fuente o usar la fuente por defecto del juego"""
    # Fuente por defecto del juego
    default_font = "04B_11__.TTF"
    
    if font_name is None:
        font_name = default_font
    
    font_path = os.path.join(FONTS_DIR, font_name)
    if os.path.exists(font_path):
        try:
            return pygame.font.Font(font_path, size)
        except:
            pass
    return pygame.font.Font(None, size)

def load_image(filename: str):
    """Cargar una imagen del directorio img"""
    img_path = os.path.join(IMG_DIR, filename)
    if os.path.exists(img_path):
        return pygame.image.load(img_path).convert_alpha()
    return None

