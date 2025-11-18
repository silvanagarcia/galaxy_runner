"""
Escena de Game Over
"""

import pygame
from ..ui import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED, GREEN, load_font

class GameOverScene:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font_large = load_font(72)
        self.font_medium = load_font(48)
        self.font_small = load_font(24)
        self.player_name = ""
        self.entering_name = True
        self.score = 0
        self.level = 1
        
    def handle_event(self, event: pygame.event.Event) -> str:
        """
        Manejar eventos
        """
        if event.type == pygame.KEYDOWN:
            if self.entering_name:
                if event.key == pygame.K_RETURN:
                    if self.player_name.strip():
                        self.entering_name = False
                        return 'save_score'
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                else:
                    if len(self.player_name) < 15:
                        char = event.unicode
                        if char.isalnum() or char == ' ':
                            self.player_name += char
            else:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return 'menu'
        return None
    
    def set_score(self, score: int, level: int):
        """
        Establecer puntuación y nivel alcanzado
        """
        self.score = score
        self.level = level
    
    def get_player_name(self) -> str:
        """
        Obtener nombre del jugador
        """
        return self.player_name.strip()
    
    def reset(self):
        """Reiniciar el estado de la escena"""
        self.player_name = ""
        self.entering_name = True
    
    def draw(self):
        """
        Dibujar la pantalla de game over
        """
        self.screen.fill(BLACK)
        
        # Título
        title = self.font_large.render("GAME OVER", True, RED)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        self.screen.blit(title, title_rect)
        
        # Puntuación
        score_text = self.font_medium.render(f"Puntuacion: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(score_text, score_rect)
        
        level_text = self.font_medium.render(f"Nivel alcanzado: {self.level}", True, WHITE)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(level_text, level_rect)
        
        if self.entering_name:
            # Entrada de nombre
            name_prompt = self.font_small.render("Ingresa tu nombre:", True, WHITE)
            name_prompt_rect = name_prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(name_prompt, name_prompt_rect)
            
            name_display = self.font_medium.render(self.player_name + "_", True, GREEN)
            name_display_rect = name_display.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            self.screen.blit(name_display, name_display_rect)
            
            enter_text = self.font_small.render("Presiona ENTER para guardar", True, WHITE)
            enter_rect = enter_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
            self.screen.blit(enter_text, enter_rect)
        else:
            # Confirmación
            saved_text = self.font_small.render("Puntuacion guardada!", True, GREEN)
            saved_rect = saved_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(saved_text, saved_rect)
            
            continue_text = self.font_small.render("Presiona ENTER para volver al menu", True, WHITE)
            continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            self.screen.blit(continue_text, continue_rect)

