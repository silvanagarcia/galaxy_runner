### Sistema de enemigos


import os
import pygame
import random
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from galaxy_runner.ui import SCREEN_WIDTH, SCREEN_HEIGHT, PROJECTILE_SPEED
from galaxy_runner.entities.proyectiles import Projectile
from galaxy_runner.paths import get_image_path

class Enemy:
    def __init__(self, x: int, y: int, speed: float, level: int = 1):
        self.x = x
        self.y = y
        self.width = 45
        self.height = 45
        self.speed = speed
        self.level = level
        
        # Movimiento aleatorio
        self.direction_x = random.choice([-1, 1]) * random.uniform(0.5, 1.0)
        self.direction_y = random.choice([-1, 1]) * random.uniform(0.3, 0.7)
        self.change_direction_timer = random.uniform(1.0, 3.0)
        
        # Rectángulo para colisiones
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Cooldown de disparo
        self.shoot_cooldown = random.uniform(1.0, 3.0)
        self.shoot_delay = random.uniform(2.0, 4.0)
        
        # Límite de movimiento (mitad superior de la pantalla)
        self.max_y = SCREEN_HEIGHT // 2
        
        # Imagen del enemigo
        self.image = None
        try:
            img_path = get_image_path('enemigo.png')
            if os.path.exists(img_path):
                self.image = pygame.transform.scale(
                    pygame.image.load(img_path).convert_alpha(),
                    (self.width, self.height)
                )
        except Exception as e:
            print(f"No se pudo cargar la imagen del enemigo: {e}")

    def update(self, dt: float) -> bool:
        # Cambiar dirección aleatoriamente
        self.change_direction_timer -= dt
        if self.change_direction_timer <= 0:
            self.direction_x = random.choice([-1, 1]) * random.uniform(0.5, 1.0)
            self.direction_y = random.choice([-1, 1]) * random.uniform(0.3, 0.7)
            self.change_direction_timer = random.uniform(1.0, 3.0)

        # Movimiento aleatorio
        self.x += self.speed * self.direction_x * dt
        self.y += self.speed * self.direction_y * dt

        # Limitar dentro de los bordes horizontales
        if self.x <= 0:
            self.x = 0
            self.direction_x *= -1
        elif self.x >= SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
            self.direction_x *= -1

        # Limitar a la mitad superior de la pantalla
        if self.y <= 0:
            self.y = 0
            self.direction_y *= -1
        elif self.y >= self.max_y - self.height:
            self.y = self.max_y - self.height
            self.direction_y *= -1

        # Actualizar rectángulo
        self.rect.x = self.x
        self.rect.y = self.y

        # Actualizar cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

        return True

    def shoot(self) -> 'Projectile':
        if self.shoot_cooldown <= 0:
            self.shoot_cooldown = self.shoot_delay
            from galaxy_runner.entities.proyectiles import Projectile

            return Projectile(
                self.x + self.width // 2,
                self.y + self.height,
                PROJECTILE_SPEED * 1.3,
                is_player=False
            )
        return None

    def draw(self, screen: pygame.Surface):
        ### Dibujar el enemigo
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            # Forma básica: cuadrado
            pygame.draw.rect(screen, (255, 0, 0), self.rect)
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)