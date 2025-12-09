

import pygame
import os


class Explosion:
    def __init__(self, x: int, y: int, size: int = 50):
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(x - size//2, y - size//2, size, size)
        
        # Animación simple
        self.frames = 0
        self.max_frames = 10
        self.finished = False
        
        # Color de la explosión
        self.colors = [
            (255, 255, 0),   # Amarillo
            (255, 200, 0),   # Naranja claro
            (255, 150, 0),   # Naranja
            (255, 100, 0),   # Naranja oscuro
            (255, 50, 0),    # Rojo naranja
            (200, 0, 0),     # Rojo
        ]
    
    def update(self, dt: float = 0):
        
        self.frames += 1
        if self.frames >= self.max_frames:
            self.finished = True
            return False
        return True
    
    def draw(self, screen: pygame.Surface):
        
        if not self.finished:
            # Calcular tamaño de la explosión basado en el frame
            progress = self.frames / self.max_frames
            current_size = int(self.size * (1 + progress * 0.5))
            
            # Obtener color actual
            color_index = min(int(progress * len(self.colors)), len(self.colors) - 1)
            color = self.colors[color_index]
            
            # Dibujar círculo de explosión
            pygame.draw.circle(
                screen,
                color,
                (int(self.x), int(self.y)),
                current_size // 2
            )
            
            # Dibujar círculo interno más brillante
            inner_color = tuple(min(255, c + 50) for c in color)
            pygame.draw.circle(
                screen,
                inner_color,
                (int(self.x), int(self.y)),
                current_size // 4
            )
    
    def is_finished(self) -> bool:
        
        return self.finished
