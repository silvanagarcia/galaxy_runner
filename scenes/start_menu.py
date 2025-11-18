"""
Escena del menú de inicio
"""

import pygame
from ..ui import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GREEN, load_font

class StartMenuScene:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font_large = load_font(72)
        self.font_medium = load_font(36)
        self.font_small = load_font(24)
        
    def handle_event(self, event: pygame.event.Event) -> str:
        """
        Manejar eventos. Retorna 'start' si se presiona Enter
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return 'start'
        return None
    
    def draw(self):
        """
        Dibujar el menú
        """
        self.screen.fill(BLACK)
        
        # Título
        title = self.font_large.render("GALAXY RUNNER", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(title, title_rect)
        
        # Instrucciones
        text1 = self.font_medium.render("Presiona ENTER o ESPACIO para comenzar", True, GREEN)
        text1_rect = text1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text1, text1_rect)
        
        text2 = self.font_small.render("Flechas o WASD: Mover | ESPACIO: Disparar", True, WHITE)
        text2_rect = text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(text2, text2_rect)
        
        text3 = self.font_small.render("L.SHIFT: Sprint (cada 5s) | R: Ranking | ESC: Salir", True, WHITE)
        text3_rect = text3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(text3, text3_rect)

