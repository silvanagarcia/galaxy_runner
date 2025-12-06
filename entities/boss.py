### Sistema de jefes



import pygame
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from galaxy_runner.ui import SCREEN_WIDTH, SCREEN_HEIGHT
from galaxy_runner.entities.proyectiles import Projectile
from galaxy_runner.ui import PROJECTILE_SPEED
from galaxy_runner.paths import get_image_path

class Boss:
    def __init__(self, level: int):
        self.level = level
        self.width = 80 + (level * 20)
        self.height = 60 + (level * 15)
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = 50
        self.speed = 190 + (level * 30)
        self.direction = 1
        self.max_health = 75 + (level * 30)
        self.health = self.max_health

        # Rectángulo para colisiones
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Imagen del jefe según el nivel
        self.image = None
        try:
            img_path = get_image_path(f'boss_{self.level}.png')
            if os.path.exists(img_path):
                self.image = pygame.transform.scale(
                    pygame.image.load(img_path).convert_alpha(),
                    (self.width, self.height)
                )
        except Exception as e:
            print(f"No se pudo cargar la imagen del boss: {e}")

        # Cooldown de disparo (más rápido en niveles superiores)
        self.shoot_cooldown = 0
        self.shoot_delay = 1.8 - (level * 0.2)
        self.shoot_delay = max(0.5, self.shoot_delay)

    def update(self, dt: float):
        ### Actualizar posición del jefe
        # Movimiento horizontal con rebote
        self.x += self.speed * self.direction * dt

        # Cambiar dirección si llega a los bordes
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
            self.direction *= -1

        # Actualizar rectángulo
        self.rect.x = self.x
        self.rect.y = self.y

        # Actualizar cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

    def shoot(self) -> list:
        ### Disparar proyectiles (múltiples en niveles superiores)
        projectiles = []
        if self.shoot_cooldown <= 0:
            self.shoot_cooldown = self.shoot_delay

            from galaxy_runner.entities.proyectiles import Projectile

            # Nivel 1: 1 proyectil
            # Nivel 2: 2 proyectiles
            # Nivel 3: 3 proyectiles
            num_projectiles = min(self.level, 3)

            if num_projectiles == 1:
                projectiles.append(Projectile(
                    self.x + self.width // 2,
                    self.y + self.height,
                    PROJECTILE_SPEED * 1.2,
                    is_player=False,
                    is_boss=True  # Proyectil de boss
                ))
            else:
                # Disparar en abanico
                spread = 30
                start_angle = -spread * (num_projectiles - 1) / 2
                for i in range(num_projectiles):
                    angle = start_angle + (i * spread)
                    # Simplificado: proyectiles en diferentes posiciones X
                    offset_x = (i - (num_projectiles - 1) / 2) * 20
                    projectiles.append(Projectile(
                        self.x + self.width // 2 + offset_x,
                        self.y + self.height,
                        PROJECTILE_SPEED * 0.8,
                        is_player=False,
                        is_boss=True  # Proyectil de boss
                    ))

        return projectiles

    def take_damage(self, damage: int = 1) -> bool:
        ### Recibir daño. Retorna True si está muerto
        self.health -= damage
        return self.health <= 0

    def draw(self, screen: pygame.Surface):
        ### Dibujar el jefe
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            # Forma básica: rectángulo grande
            pygame.draw.rect(screen, (255, 0, 255), self.rect)
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 3)

        # Barra de vida
        bar_width = self.width
        bar_height = 5
        bar_x = self.x
        bar_y = self.y - 10

        # Fondo de la barra
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        # Vida actual
        health_ratio = self.health / self.max_health
        health_width = int(bar_width * health_ratio)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))