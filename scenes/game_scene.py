"""
Escena principal del juego - maneja el estado de juego
"""

import os
import pygame
import random
import sys

# Agregar directorio padre a la ruta para imports de entidades
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from ..ui import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, GREEN, YELLOW, CYAN, BLUE,
    PLAYER_SPEED, ENEMY_SPEED_BASE, METEOR_SPEED_BASE, PROJECTILE_SPEED,
    MAX_ENEMIES_ON_SCREEN, METEOR_SPAWN_INTERVAL,
    POINTS_ENEMY, POINTS_METEOR, POINTS_BOSS_1, POINTS_BOSS_2, POINTS_BOSS_3
)
from ..paths import get_image_path

from entities.player import Player
from entities.enemigos import Enemy
from entities.boss import Boss
from entities.meteorito import Meteor
from entities.proyectiles import Projectile
from entities.explosiones import Explosion
from entities.powerup import PowerUp


class GameScene:
    def __init__(self, screen: pygame.Surface, width: int, height: int):
        self.screen = screen
        self.width = width
        self.height = height
        
        # Fondo
        self.background = None
        self.background_y = 0
        self.background_speed = 100  # píxeles por segundo
        try:
            bg_path = get_image_path('fondo8bits.png')
            if os.path.exists(bg_path):
                self.background = pygame.transform.scale(
                    pygame.image.load(bg_path).convert(),
                    (width, height * 2)  # Hacerlo el doble de alto para scroll continuo
                )
        except Exception as e:
            print(f"No se pudo cargar el fondo: {e}")
        
        # Estado del juego
        self.current_level = 1
        self.max_level = 3
        
        # Efectos visuales (inicialización temprana)
        self.powerup_effect_timer = 0
        self.powerup_effect_type = None
        self.damage_effect_timer = 0
        self.pause_timer = 0
        
        # Entidades del juego
        self.reset_game()
        
    def reset_game(self):
        """Reiniciar el juego"""
        # Jugador
        self.player = Player(self.width // 2, self.height - 100)
        
        # Listas de entidades
        self.enemies = []
        self.projectiles = []
        self.meteors = []
        self.explosions = []
        self.powerups = []
        self.boss = None
        
        # Estado del nivel
        self.current_level = 1
        self.enemies_killed = 0
        self.enemies_killed_for_shield = 0
        self.boss_active = False
        self.shields_spawned_this_level = 0
        self.max_shields_per_level = 2
        
        # Requisitos de jefe por nivel
        self.boss_requirements = [30, 50, 80]
        
        # Power-ups activos
        self.rapid_fire_active = False
        self.rapid_fire_timer = 0
        self.shield_active = False
        self.shield_timer = 0
        
        # Temporizadores
        self.meteor_spawn_timer = 0
        self.boss_meteor_timer = 0
        
        # Reiniciar scroll del fondo
        self.background_y = 0
        
        # Efectos visuales
        self.powerup_effect_timer = 0
        self.powerup_effect_type = None
        self.damage_effect_timer = 0
        self.pause_timer = 0
        
        # Generar enemigos iniciales
        self.spawn_enemies()
    
    def spawn_enemies(self):
        """Generar enemigos hasta el máximo en pantalla"""
        if self.boss_active:
            return
        
        while len(self.enemies) < MAX_ENEMIES_ON_SCREEN:
            x = random.randint(0, self.width - 30)
            y = random.randint(0, self.height // 2 - 30)
            speed = ENEMY_SPEED_BASE + (self.current_level * 20)
            enemy = Enemy(x, y, speed, self.current_level)
            self.enemies.append(enemy)
    
    def spawn_meteors(self, dt: float):
        """Generar meteoritos"""
        if self.boss_active:
            self.boss_meteor_timer += dt
            if self.boss_meteor_timer >= 0.25:
                self.boss_meteor_timer = 0
                for _ in range(2):
                    x = random.randint(0, self.width - 40)
                    y = -40
                    speed = METEOR_SPEED_BASE + (self.current_level * 30)
                    meteor = Meteor(x, y, speed, self.current_level)
                    self.meteors.append(meteor)
            return
        
        self.meteor_spawn_timer += dt
        if self.meteor_spawn_timer >= METEOR_SPAWN_INTERVAL:
            self.meteor_spawn_timer = 0
            x = random.randint(0, self.width - 40)
            y = -40
            speed = METEOR_SPEED_BASE + (self.current_level * 30)
            meteor = Meteor(x, y, speed, self.current_level)
            self.meteors.append(meteor)
    
    def spawn_boss(self):
        """Generar jefe cuando se cumplan los requisitos"""
        if self.boss_active:
            return
        
        required_kills = self.boss_requirements[self.current_level - 1]
        if self.enemies_killed >= required_kills:
            self.boss = Boss(self.current_level)
            self.boss_active = True
            self.enemies.clear()
            self.boss_meteor_timer = 0
    
    def check_collisions(self):
        """Verificar todas las colisiones"""
        # Proyectiles del jugador vs enemigos
        for projectile in self.projectiles[:]:
            if not projectile.is_player:
                continue
            
            # vs enemigos
            for enemy in self.enemies[:]:
                if projectile.rect.colliderect(enemy.rect):
                    self.explosions.append(Explosion(enemy.x + enemy.width // 2, 
                                                    enemy.y + enemy.height // 2))
                    self.player.score += POINTS_ENEMY
                    self.enemies_killed += 1
                    self.enemies_killed_for_shield += 1
                    self.spawn_powerup(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2)
                    self.projectiles.remove(projectile)
                    self.enemies.remove(enemy)
                    self.spawn_enemies()
                    break
            
            # vs jefe
            if self.boss and projectile.rect.colliderect(self.boss.rect):
                boss_killed = self.boss.take_damage()
                if projectile in self.projectiles:
                    self.projectiles.remove(projectile)
                
                if boss_killed:
                    boss_x = self.boss.x + self.boss.width // 2
                    boss_y = self.boss.y + self.boss.height // 2
                    self.explosions.append(Explosion(boss_x, boss_y, 60))
                    boss_points = [POINTS_BOSS_1, POINTS_BOSS_2, POINTS_BOSS_3]
                    if 0 <= self.current_level - 1 < len(boss_points):
                        points = boss_points[self.current_level - 1]
                        self.player.score += points
                    
                    if self.current_level == 1:
                        self.spawn_powerup(boss_x - 30, boss_y, force=True, powerup_type='rapid_fire')
                        self.spawn_powerup(boss_x + 30, boss_y, force=True, powerup_type='health')
                    elif self.current_level == 2:
                        self.spawn_powerup(boss_x - 45, boss_y - 15, force=True, powerup_type='rapid_fire')
                        self.spawn_powerup(boss_x - 15, boss_y - 15, force=True, powerup_type='health')
                        self.spawn_powerup(boss_x + 45, boss_y - 15, force=True, powerup_type='health')
                    
                    self.boss = None
                    self.boss_active = False
                    
                    if self.current_level < self.max_level:
                        self.current_level += 1
                        self.enemies_killed = 0
                        self.shields_spawned_this_level = 0
                        self.enemies.clear()
                        self.meteors.clear()
                        self.projectiles = [p for p in self.projectiles if p.is_player]
                        self.powerups.clear()
                        self.meteor_spawn_timer = 0
                        self.boss_meteor_timer = 0
                        self.spawn_enemies()
                    else:
                        return 'victory'
                break
        
        # Proyectiles de enemigos vs jugador
        for projectile in self.projectiles[:]:
            if projectile.is_player:
                continue
            
            if projectile.rect.colliderect(self.player.rect):
                if not self.shield_active:
                    old_lives = self.player.lives
                    if self.player.take_damage():
                        return 'game_over'
                    # Si perdió una vida, activar efecto y pausa
                    if self.player.lives < old_lives:
                        self.damage_effect_timer = 0.5
                        self.pause_timer = 1.0  # Pausa de 1 segundo
                self.projectiles.remove(projectile)
        
        # Enemigos vs jugador
        for enemy in self.enemies[:]:
            if enemy.rect.colliderect(self.player.rect):
                if not self.shield_active:
                    old_lives = self.player.lives
                    if self.player.take_damage():
                        return 'game_over'
                    # Si perdió una vida, activar efecto y pausa
                    if self.player.lives < old_lives:
                        self.damage_effect_timer = 0.5
                        self.pause_timer = 1.0  # Pausa de 1 segundo
                self.explosions.append(Explosion(enemy.x + enemy.width // 2,
                                                enemy.y + enemy.height // 2))
                self.enemies_killed += 1
                self.enemies_killed_for_shield += 1
                self.spawn_powerup(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2)
                self.enemies.remove(enemy)
                self.spawn_enemies()
        
        # Meteoritos vs jugador
        for meteor in self.meteors[:]:
            if meteor.rect.colliderect(self.player.rect):
                if not self.shield_active:
                    old_lives = self.player.lives
                    if self.player.take_damage():
                        return 'game_over'
                    # Si perdió una vida, activar efecto y pausa
                    if self.player.lives < old_lives:
                        self.damage_effect_timer = 0.5
                        self.pause_timer = 1.0  # Pausa de 1 segundo
                self.explosions.append(Explosion(meteor.x + meteor.size // 2,
                                                meteor.y + meteor.size // 2))
                self.player.score += POINTS_METEOR
                self.meteors.remove(meteor)
        
        # Power-ups vs jugador
        for powerup in self.powerups[:]:
            if powerup.rect.colliderect(self.player.rect):
                # Activar efecto visual según el tipo de power-up
                self.powerup_effect_timer = 0.5  # 0.5 segundos de efecto
                self.powerup_effect_type = powerup.type
                
                if powerup.type == 'health':
                    self.player.lives = min(self.player.lives + 1, 3)
                elif powerup.type == 'rapid_fire':
                    self.rapid_fire_active = True
                    self.rapid_fire_timer = 10.0
                    self.player.shoot_delay = 0.1
                elif powerup.type == 'shield':
                    self.shield_active = True
                    self.shield_timer = 500
                self.powerups.remove(powerup)
        
        return None
    
    def update_powerups(self, dt: float):
        """Actualizar temporizadores de power-ups"""
        if self.rapid_fire_active:
            self.rapid_fire_timer -= dt
            if self.rapid_fire_timer <= 0:
                self.rapid_fire_active = False
                self.player.shoot_delay = 0.3
        
        if self.shield_active:
            self.shield_timer -= dt
            if self.shield_timer <= 0:
                self.shield_active = False
    
    def spawn_powerup(self, x: int, y: int, force: bool = False, powerup_type: str = None):
        """Generar power-up en una posición"""
        if force:
            powerup = PowerUp(x, y, powerup_type=powerup_type)
            self.powerups.append(powerup)
        else:
            if random.random() < 0.3:
                if powerup_type is None:
                    available_types = PowerUp.TYPES.copy()
                    if self.shields_spawned_this_level >= self.max_shields_per_level:
                        available_types.remove('shield')
                    
                    if available_types:
                        selected_type = random.choice(available_types)
                    else:
                        selected_type = random.choice(PowerUp.TYPES)
                else:
                    selected_type = powerup_type
                    if selected_type == 'shield' and self.shields_spawned_this_level >= self.max_shields_per_level:
                        available_types = [t for t in PowerUp.TYPES if t != 'shield']
                        if available_types:
                            selected_type = random.choice(available_types)
                
                if selected_type == 'shield' and self.shields_spawned_this_level < self.max_shields_per_level:
                    self.shields_spawned_this_level += 1
                
                powerup = PowerUp(x, y, powerup_type=selected_type)
                self.powerups.append(powerup)
    
    def update(self, dt: float):
        """Actualizar estado del juego"""
        # Si hay pausa activa, no actualizar nada excepto los temporizadores
        if self.pause_timer > 0:
            self.pause_timer -= dt
            # Actualizar solo efectos visuales durante la pausa
            if self.powerup_effect_timer > 0:
                self.powerup_effect_timer -= dt
            if self.damage_effect_timer > 0:
                self.damage_effect_timer -= dt
            return None
        
        keys = pygame.key.get_pressed()
        
        # Actualizar efectos visuales
        if self.powerup_effect_timer > 0:
            self.powerup_effect_timer -= dt
        if self.damage_effect_timer > 0:
            self.damage_effect_timer -= dt
        
        # Actualizar scroll del fondo
        if self.background:
            self.background_y += self.background_speed * dt
            if self.background_y >= self.height:
                self.background_y = 0
        
        # Actualizar jugador
        self.player.update(dt, keys)
        
        # Disparo del jugador
        if keys[pygame.K_SPACE]:
            projectile = self.player.shoot()
            if projectile:
                self.projectiles.append(projectile)
        
        # Generar enemigos
        self.spawn_enemies()
        
        # Generar meteoritos
        self.spawn_meteors(dt)
        
        # Generar jefe cuando se cumplan los requisitos
        if not self.boss_active:
            self.spawn_boss()
        
        # Actualizar enemigos
        for enemy in self.enemies[:]:
            if not enemy.update(dt):
                self.enemies.remove(enemy)
            else:
                projectile = enemy.shoot()
                if projectile:
                    self.projectiles.append(projectile)
        
        # Actualizar jefe
        if self.boss:
            self.boss.update(dt)
            projectiles = self.boss.shoot()
            self.projectiles.extend(projectiles)
        
        # Actualizar meteoritos
        for meteor in self.meteors[:]:
            if not meteor.update(dt):
                self.meteors.remove(meteor)
        
        # Actualizar proyectiles
        for projectile in self.projectiles[:]:
            if not projectile.update(dt):
                self.projectiles.remove(projectile)
        
        # Actualizar power-ups
        for powerup in self.powerups[:]:
            if not powerup.update(dt):
                self.powerups.remove(powerup)
        
        # Actualizar explosiones
        for explosion in self.explosions[:]:
            if not explosion.update(dt):
                self.explosions.remove(explosion)
        
        # Actualizar power-ups activos
        self.update_powerups(dt)
        
        # Verificar colisiones
        result = self.check_collisions()
        return result
    
    def draw(self):
        """Dibujar el juego"""
        # Dibujar fondo con scroll
        if self.background:
            # Dibujar primer fondo
            self.screen.blit(self.background, (0, self.background_y - self.height))
            # Dibujar segundo fondo para loop continuo
            self.screen.blit(self.background, (0, self.background_y))
        else:
            self.screen.fill(BLACK)
        
        # Dibujar entidades
        self.player.draw(self.screen)
        
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        if self.boss:
            self.boss.draw(self.screen)
        
        for meteor in self.meteors:
            meteor.draw(self.screen)
        
        for projectile in self.projectiles:
            projectile.draw(self.screen)
        
        for powerup in self.powerups:
            powerup.draw(self.screen)
        
        for explosion in self.explosions:
            explosion.draw(self.screen)
        
        # Visualización del escudo
        if self.shield_active:
            pygame.draw.circle(self.screen, (0, 255, 255), 
                             (int(self.player.x + self.player.width // 2),
                              int(self.player.y + self.player.height // 2)),
                             self.player.width + 10, 2)
        
        # Efecto visual de power-up
        if self.powerup_effect_timer > 0:
            alpha = int(128 * (self.powerup_effect_timer / 0.5))  # Fade out
            if self.powerup_effect_type == 'health':
                # Flash verde para salud
                overlay = pygame.Surface((self.width, self.height))
                overlay.set_alpha(alpha)
                overlay.fill((0, 255, 0))
                self.screen.blit(overlay, (0, 0))
            elif self.powerup_effect_type == 'rapid_fire':
                # Flash cian para disparo rápido
                overlay = pygame.Surface((self.width, self.height))
                overlay.set_alpha(alpha)
                overlay.fill((0, 255, 255))
                self.screen.blit(overlay, (0, 0))
            elif self.powerup_effect_type == 'shield':
                # Flash azul para escudo
                overlay = pygame.Surface((self.width, self.height))
                overlay.set_alpha(alpha)
                overlay.fill((0, 100, 255))
                self.screen.blit(overlay, (0, 0))
        
        # Efecto visual de daño
        if self.damage_effect_timer > 0:
            alpha = int(150 * (self.damage_effect_timer / 0.5))  # Fade out
            # Flash rojo para daño
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(alpha)
            overlay.fill((255, 0, 0))
            self.screen.blit(overlay, (0, 0))
        
        # Mostrar mensaje durante la pausa
        if self.pause_timer > 0:
            from ..ui import load_font
            pause_font = load_font(48)
            pause_text = pause_font.render("¡VIDA PERDIDA!", True, (255, 255, 255))
            pause_rect = pause_text.get_rect(center=(self.width // 2, self.height // 2))
            # Fondo semitransparente para el texto
            text_bg = pygame.Surface((pause_rect.width + 40, pause_rect.height + 20))
            text_bg.set_alpha(200)
            text_bg.fill((0, 0, 0))
            self.screen.blit(text_bg, (pause_rect.x - 20, pause_rect.y - 10))
            self.screen.blit(pause_text, pause_rect)
        
        # Interfaz de usuario
        from ..ui import load_font
        font = load_font(36)
        
        # Vidas
        lives_text = font.render(f"Vidas: {self.player.lives}", True, WHITE)
        self.screen.blit(lives_text, (10, 10))
        
        # Puntuación
        score_text = font.render(f"Puntuacion: {self.player.score}", True, WHITE)
        self.screen.blit(score_text, (10, 50))
        
        # Nivel
        level_text = font.render(f"Nivel: {self.current_level}", True, WHITE)
        self.screen.blit(level_text, (10, 90))
        
        # Enemigos eliminados / Requisitos de jefe
        required = self.boss_requirements[self.current_level - 1]
        kills_text = font.render(f"Esbirros: {self.enemies_killed}/{required}", True, WHITE)
        self.screen.blit(kills_text, (10, 130))
        
        # Cooldown de sprint
        if self.player.sprint_cooldown > 0:
            sprint_text = font.render(f"Sprint: {int(self.player.sprint_cooldown)}s", True, YELLOW)
            self.screen.blit(sprint_text, (10, 170))
        elif self.player.sprint_active:
            sprint_text = font.render("SPRINT ACTIVO!", True, GREEN)
            self.screen.blit(sprint_text, (10, 170))
        
        # Power-ups activos
        y_offset = 210
        if self.rapid_fire_active:
            rapid_text = font.render(f"Disparo Rapido: {int(self.rapid_fire_timer)}s", True, CYAN)
            self.screen.blit(rapid_text, (10, y_offset))
            y_offset += 40
        
        if self.shield_active:
            shield_text = font.render(f"Escudo: {int(self.shield_timer)}s", True, BLUE)
            self.screen.blit(shield_text, (10, y_offset))
    
    def get_score(self):
        """Obtener puntuación actual"""
        return self.player.score
    
    def get_level(self):
        """Obtener nivel actual"""
        return self.current_level

