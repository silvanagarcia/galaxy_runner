### Sistema de meteoritos

import os
import pygame
import random
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from UI.ui import SCREEN_WIDTH, SCREEN_HEIGHT
from constants.config import get_image_path

class Meteor:
    def __init__(self, x: int, y: int, speed: float, level: int = 1, direction: tuple = (0, 1)):
        self.x = x
        self.y = y
        self.size = random.randint(30, 40)
        self.speed = speed + (level * 50)
        self.rotation = 0
        self.rotation_speed = random.uniform(-180, 180)
        self.direction = direction  # (dx, dy) dirección de movimiento normalizada
        
        # Rectángulo para colisiones
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

        # Imagen del meteorito
        self.image = None
        try:
            img_path = get_image_path('meteorito.png')
            if os.path.exists(img_path):
                self.image = pygame.transform.scale(
                    pygame.image.load(img_path).convert_alpha(),
                    (self.size, self.size)
                )
            else:
                print(f"No se encontró la imagen del meteorito en {img_path}")
        except Exception as e:
            print(f"No se pudo cargar la imagen del meteorito: {e}")

    def update(self, dt: float) -> bool:

        ### Actualizar posición. Retorna False si está fuera de pantalla

        # Movimiento en la dirección especificada
        self.x += self.speed * self.direction[0] * dt
        self.y += self.speed * self.direction[1] * dt
        
        # Rotación
        self.rotation += self.rotation_speed * dt
        
        # Actualizar rectángulo
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Eliminar si está fuera de pantalla
        if (self.y > SCREEN_HEIGHT or self.y < -self.size or 
            self.x > SCREEN_WIDTH or self.x < -self.size):
            return False
        return True
    
    def draw(self, screen: pygame.Surface):

        ### Dibujar el meteorito
        if self.image:
            # Rotar la imagen según self.rotation
            rotated_image = pygame.transform.rotate(self.image, self.rotation)
            rect = rotated_image.get_rect(center=(self.x + self.size // 2, self.y + self.size // 2))
            screen.blit(rotated_image, rect.topleft)
        else:
            # Forma básica: círculo/elipse
            pygame.draw.ellipse(screen, (139, 69, 19), self.rect)  # Marrón
            pygame.draw.ellipse(screen, (255, 255, 255), self.rect, 2)

