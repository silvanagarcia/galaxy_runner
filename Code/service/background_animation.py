### Background Animation Manager - Sistema de animación de fondo para Galaxy Runner

import pygame
import os
from typing import List, Optional

class BackgroundAnimation:
    def __init__(self, screen_width: int, screen_height: int):

        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Lista para almacenar los frames de la animación
        self.frames: List[pygame.Surface] = []
        
        # Control de animación
        self.current_frame = 0
        self.frame_timer = 0.0
        self.frame_duration = 0.1  # Duración de cada frame en segundos (10 FPS)
        self.total_frames = 14
        
        # Estado de la animación
        self.animation_enabled = True
        self.loop_animation = True
        
        # Cargar frames de animación
        self.load_frames()
    
    def load_frames(self):

        from Code.constants.config import BACKGROUNDS_DIR
        
        self.frames.clear()
        frames_loaded = 0
        
        for i in range(1, self.total_frames + 1):
            frame_name = f"bg_{i:02d}.png"  # bg_01.png, bg_02.png, etc.
            full_path = os.path.join(BACKGROUNDS_DIR, frame_name)
            
            try:
                if os.path.exists(full_path):
                    # Cargar imagen y escalarla al tamaño de pantalla
                    frame = pygame.image.load(full_path).convert()
                    frame = pygame.transform.scale(frame, (self.screen_width, self.screen_height))
                    self.frames.append(frame)
                    frames_loaded += 1
                    print(f"Frame de fondo cargado: {frame_name}")
                else:
                    print(f"Frame de fondo no encontrado: {full_path}")
                    # Crear frame placeholder si no existe el archivo
                    placeholder = self.create_placeholder_frame(i)
                    self.frames.append(placeholder)
            except Exception as e:
                print(f"Error al cargar frame {frame_name}: {e}")
                # Crear frame placeholder en caso de error
                placeholder = self.create_placeholder_frame(i)
                self.frames.append(placeholder)
        
        print(f"Sistema de animación de fondo inicializado: {frames_loaded}/{self.total_frames} frames cargados")
        
        # Si no se cargó ningún frame, crear frames placeholder
        if not self.frames:
            self.create_default_frames()
    
    def create_placeholder_frame(self, frame_number: int) -> pygame.Surface:

        frame = pygame.Surface((self.screen_width, self.screen_height))
        
        # Crear un gradiente de colores espaciales como placeholder
        colors = [
            (10, 10, 30),    # Azul oscuro
            (20, 10, 50),    # Púrpura oscuro
            (30, 20, 60),    # Púrpura
            (15, 25, 45),    # Azul medio
            (25, 15, 55),    # Púrpura medio
        ]
        
        color_index = (frame_number - 1) % len(colors)
        base_color = colors[color_index]
        
        # Crear gradiente vertical
        for y in range(self.screen_height):
            intensity = y / self.screen_height
            color = (
                int(base_color[0] * (1 + intensity * 0.5)),
                int(base_color[1] * (1 + intensity * 0.3)),
                int(base_color[2] * (1 + intensity * 0.7))
            )
            # Limitar valores a 255
            color = tuple(min(255, max(0, c)) for c in color)
            pygame.draw.line(frame, color, (0, y), (self.screen_width, y))
        
        # Agregar algunas "estrellas" para efecto espacial
        import random
        random.seed(frame_number * 42)  # Seed fijo para consistencia
        for _ in range(50):
            x = random.randint(0, self.screen_width - 1)
            y = random.randint(0, self.screen_height - 1)
            brightness = random.randint(100, 255)
            star_color = (brightness, brightness, brightness)
            pygame.draw.circle(frame, star_color, (x, y), 1)
        
        return frame
    
    def create_default_frames(self):

        print("Creando frames de animación por defecto...")
        for i in range(self.total_frames):
            frame = self.create_placeholder_frame(i + 1)
            self.frames.append(frame)
    
    def update(self, dt: float):

        if not self.animation_enabled or not self.frames:
            return
        
        self.frame_timer += dt
        
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0.0
            self.current_frame += 1
            
            if self.current_frame >= len(self.frames):
                if self.loop_animation:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
    
    def draw(self, screen: pygame.Surface):

        if not self.animation_enabled or not self.frames:
            # Si no hay animación, llenar con color negro
            screen.fill((0, 0, 0))
            return
        
        if 0 <= self.current_frame < len(self.frames):
            screen.blit(self.frames[self.current_frame], (0, 0))
        else:
            # Fallback: llenar con color negro
            screen.fill((0, 0, 0))
    
    def set_frame_duration(self, duration: float):

        self.frame_duration = max(0.01, duration)  # Mínimo 0.01 segundos
    
    def set_animation_enabled(self, enabled: bool):

        self.animation_enabled = enabled
    
    def reset_animation(self):

        self.current_frame = 0
        self.frame_timer = 0.0
    
    def get_current_frame_info(self) -> dict:

        return {
            'current_frame': self.current_frame + 1,
            'total_frames': len(self.frames),
            'frame_timer': self.frame_timer,
            'frame_duration': self.frame_duration,
            'animation_enabled': self.animation_enabled
        }
    
    def reload_frames(self):

        print("Recargando frames de animación de fondo...")
        self.load_frames()
        self.reset_animation()
