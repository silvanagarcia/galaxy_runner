"""
Escena de Game Over
"""

import pygame
from UI.ui import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED, load_font


class GameOverScene:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font_large = load_font(72)
        self.font_medium = load_font(48)
        self.font_small = load_font(24)
        
        self.score = 0
        self.level = 0
        self.player_name = ""
        self.entering_name = True
        
    def set_score(self, score: int, level: int):
        """Establecer puntuación y nivel"""
        self.score = score
        self.level = level
    
    def reset(self):
        """Resetear estado"""
        self.player_name = ""
        self.entering_name = True
    
    def get_player_name(self) -> str:
        """Obtener nombre del jugador"""
        return self.player_name if self.player_name else None
    
    def handle_event(self, event: pygame.event.Event) -> str:
        """Manejar eventos"""
        if event.type == pygame.KEYDOWN:
            if self.entering_name:
                if event.key == pygame.K_RETURN:
                    if len(self.player_name) > 0:
                        self.entering_name = False
                        return 'save_score'
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                else:
                    # Agregar carácter al nombre (máximo 15 caracteres)
                    if len(self.player_name) < 15 and event.unicode.isprintable():
                        self.player_name += event.unicode
            else:
                # Después de guardar, presionar cualquier tecla regresa al menú
                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    return 'menu'
        return None
    
    def draw(self):
        """Dibujar pantalla de Game Over"""
        self.screen.fill(BLACK)
        
        # Título
        title = self.font_large.render("GAME OVER", True, RED)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))
        self.screen.blit(title, title_rect)
        
        # Puntuación
        score_text = self.font_medium.render(f"Puntuacion: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(score_text, score_rect)
        
        # Nivel
        level_text = self.font_medium.render(f"Nivel: {self.level}", True, WHITE)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(level_text, level_rect)
        
        # Entrada de nombre
        if self.entering_name:
            prompt = self.font_small.render("Ingresa tu nombre:", True, WHITE)
            prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(prompt, prompt_rect)
            
            name_text = self.font_medium.render(self.player_name + "_", True, WHITE)
            name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
            self.screen.blit(name_text, name_rect)
            
            instruction = self.font_small.render("Presiona ENTER para guardar", True, WHITE)
            instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
            self.screen.blit(instruction, instruction_rect)
        else:
            saved = self.font_small.render("Puntuacion guardada!", True, WHITE)
            saved_rect = saved.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(saved, saved_rect)
            
            menu_text = self.font_small.render("Presiona ENTER para volver al menu", True, WHITE)
            menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            self.screen.blit(menu_text, menu_rect)
