### Sistema de proyectiles

import os
import pygame
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from UI.ui import SCREEN_WIDTH, SCREEN_HEIGHT
from constants.config import get_image_path

class Projectile:
    def __init__(self, x: int, y: int, speed: float, is_player: bool = True, is_boss: bool = False, width: int = None, height: int = None):
        self.x = x
        self.y = y

        # Tamaño personalizado
        self.width = width if width is not None else (30 if is_boss else 16)
        self.height = height if height is not None else (48 if is_boss else 30)
        self.speed = speed
        self.is_player = is_player
        self.is_boss = is_boss
        
        # Rectángulo para colisiones
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.image = None

        try:
            if self.is_player:
                img_path = get_image_path('proyectil_player.png')
            elif self.is_boss:
                img_path = get_image_path('proyectil_boss.png')
            else:
                img_path = get_image_path('proyectil_enemigo.png')
            if os.path.exists(img_path):
                self.image = pygame.transform.scale(pygame.image.load(img_path).convert_alpha(), (self.width, self.height))
        except Exception as e:
            print(f"No se pudo cargar la imagen del proyectil: {e}")

    def update(self, dt: float) -> bool:

        ### Actualizar posición. Retorna False si está fuera de pantalla

        self.y += self.speed * dt
        self.rect.y = self.y
        
        # Eliminar si está fuera de pantalla
        if self.y < -self.height or self.y > SCREEN_HEIGHT:
            return False
        return True
    
    def draw(self, screen: pygame.Surface):
        
        ### Dibujar el proyectil
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            color = (255, 255, 0) if self.is_player else (255, 0, 0)
            pygame.draw.rect(screen, color, self.rect)

