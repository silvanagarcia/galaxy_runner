


import pygame
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from UI.ui import PLAYER_SPEED, PROJECTILE_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT
from entities.proyectiles import Projectile
from constants.config import get_image_path

class Player:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.width = 70
        self.height = 80
        self.base_speed = PLAYER_SPEED
        self.speed = PLAYER_SPEED
        self.sprint_multiplier = 2.0  # Multiplicador de velocidad al sprintar
        self.lives = 3
        self.score = 0
        
        # Rectángulo para colisiones
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Cooldown de disparo
        self.shoot_cooldown = 0
        self.shoot_delay = 0.05  # segundos entre disparos
        
        # Sprint
        self.sprint_cooldown = 0
        self.sprint_duration = 0
        self.sprint_active = False
        self.sprint_cooldown_time = 4.0  # 5 segundos de cooldown
        self.sprint_duration_time = 1  # Duración del sprint

        # Cargar imágenes de la nave para animación (centro, izquierda, derecha)
        self.image_center = None
        self.image_left = None
        self.image_right = None
        try:
            img_center = get_image_path('player.png')
            img_left = get_image_path('player_izquierda.png')
            img_right = get_image_path('player_derecha.png')
            if os.path.exists(img_center):
                self.image_center = pygame.transform.scale(pygame.image.load(img_center).convert_alpha(), (self.width, self.height))
            if os.path.exists(img_left):
                self.image_left = pygame.transform.scale(pygame.image.load(img_left).convert_alpha(), (self.width, self.height))
            if os.path.exists(img_right):
                self.image_right = pygame.transform.scale(pygame.image.load(img_right).convert_alpha(), (self.width, self.height))
        except Exception as e:
            print(f"No se pudieron cargar las imágenes del player: {e}")
        self.image = self.image_center  # Por compatibilidad
        
    def update(self, dt: float, keys: pygame.key.ScancodeWrapper):
        
        ### Actualizar posición del jugador

        # Manejar sprint
        if keys[pygame.K_LSHIFT] and self.sprint_cooldown <= 0 and not self.sprint_active:
            self.sprint_active = True
            self.sprint_duration = self.sprint_duration_time
            self.speed = self.base_speed * self.sprint_multiplier
        
        # Actualizar sprint
        if self.sprint_active:
            self.sprint_duration -= dt
            if self.sprint_duration <= 0:
                self.sprint_active = False
                self.speed = self.base_speed
                self.sprint_cooldown = self.sprint_cooldown_time
        
        # Actualizar cooldown de sprint
        if self.sprint_cooldown > 0 and not self.sprint_active:
            self.sprint_cooldown -= dt
        
        # Movimiento
        dx = 0
        dy = 0
        
        # Guardar la última dirección para la animación
        self.last_direction = 'center'
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.speed * dt
            self.last_direction = 'left'
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed * dt
            self.last_direction = 'right'
        else:
            self.last_direction = 'center'
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= self.speed * dt
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += self.speed * dt
        
        # Actualizar posición
        self.x += dx
        self.y += dy
        
        # Limitar dentro de la pantalla
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))
        
        # Actualizar rectángulo
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Actualizar cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt
    
    def shoot(self) -> 'Projectile':
        
        ### Disparar un proyectil

        if self.shoot_cooldown <= 0:
            self.shoot_cooldown = self.shoot_delay
            from entities.proyectiles import Projectile
            return Projectile(
                self.x + self.width // 2,
                self.y,
                -PROJECTILE_SPEED,
                is_player=True
            )
        return None
    
    def take_damage(self):

        ### Recibir daño

        self.lives -= 1
        return self.lives <= 0
    
    def draw(self, screen: pygame.Surface):
        
        ### Dibujar el jugador (usa imagen si está disponible, si no, triángulo)
        
        # Seleccionar imagen según dirección
        image_to_draw = self.image_center
        if hasattr(self, 'last_direction'):
            if self.last_direction == 'left' and self.image_left:
                image_to_draw = self.image_left
            elif self.last_direction == 'right' and self.image_right:
                image_to_draw = self.image_right
            elif self.image_center:
                image_to_draw = self.image_center
        if image_to_draw:
            screen.blit(image_to_draw, (self.x, self.y))
        else:
            # Forma básica: triángulo apuntando hacia arriba
            points = [
                (self.x + self.width // 2, self.y),
                (self.x, self.y + self.height),
                (self.x + self.width, self.y + self.height)
            ]
            pygame.draw.polygon(screen, (0, 255, 0), points)
            pygame.draw.polygon(screen, (255, 255, 255), points, 2)

