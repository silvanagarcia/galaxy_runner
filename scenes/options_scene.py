"""
Escena de opciones
"""

import pygame
from ..ui import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GREEN, load_font

class OptionsScene:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font_large = load_font(72)
        self.font_medium = load_font(36)
        self.font_small = load_font(24)
        
    def handle_event(self, event: pygame.event.Event) -> str:
        """
        Manejar eventos. Retorna 'menu' si se presiona ESC
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                return 'menu'
        return None
    
    def draw(self):
        """
        Dibujar la pantalla de opciones
        """
        self.screen.fill(BLACK)
        
        # Título
        title = self.font_large.render("OPCIONES", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))
        self.screen.blit(title, title_rect)
        
        # Texto placeholder
        text = self.font_medium.render("Opciones del juego", True, GREEN)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
        
        instruction = self.font_small.render("Presiona ESC para volver", True, WHITE)
        instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(instruction, instruction_rect)

