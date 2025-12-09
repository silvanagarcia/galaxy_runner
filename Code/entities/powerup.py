### Sistema de power-ups


import pygame
import random
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from UI.ui import SCREEN_HEIGHT
from constants.config import get_image_path

class PowerUp:
    TYPES = ['health', 'rapid_fire', 'shield']
    
    def __init__(self, x: int, y: int, powerup_type: str = None):
        self.x = x
        self.y = y
        self.width = 70
        self.height = 70
        self.speed = 100
        self.type = powerup_type if powerup_type in self.TYPES else random.choice(self.TYPES)
        self.rotation = 0
        
        # Rectángulo para colisiones
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Imagen según tipo
        self.image = None
        try:
            img_map = {
                'health': get_image_path('powerup_health.png'),
                'rapid_fire': get_image_path('powerup_rapid_fire.png'),
                'shield': get_image_path('powerup_shield.png'),
            }
            img_path = img_map.get(self.type)
            if img_path and os.path.exists(img_path):
                self.image = pygame.transform.scale(pygame.image.load(img_path).convert_alpha(), (self.width, self.height))
        except Exception as e:
            print(f"No se pudo cargar la imagen del power-up: {e}")
        
    def update(self, dt: float) -> bool:

        ### Actualizar posición. Retorna False si está fuera de pantalla"""
        
        self.y += self.speed * dt
        self.rotation += 90 * dt
        
        self.rect.y = self.y
        
        if self.y > SCREEN_HEIGHT:
            return False
        return True
    
    def draw(self, screen: pygame.Surface):

        ### Dibujar el power-up
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            # Colores según tipo
            colors = {
                'health': (255, 0, 0),      # Rojo para vida
                'rapid_fire': (0, 255, 255), # Cyan para disparo rápido
                'shield': (0, 0, 255)        # Azul para escudo
            }
            
            color = colors.get(self.type, (255, 255, 255))
            
            # Forma básica: rombo
            points = [
                (self.x + self.width // 2, self.y),
                (self.x + self.width, self.y + self.height // 2),
                (self.x + self.width // 2, self.y + self.height),
                (self.x, self.y + self.height // 2)
            ]
            pygame.draw.polygon(screen, color, points)
            pygame.draw.polygon(screen, (255, 255, 255), points, 2)

