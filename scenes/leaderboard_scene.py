"""
Escena del ranking
"""

import pygame
from ..ui import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, YELLOW, GREEN, load_font

class LeaderboardScene:
    def __init__(self, screen: pygame.Surface, database):
        self.screen = screen
        self.database = database
        self.font_large = load_font(72)
        self.font_medium = load_font(36)
        self.font_small = load_font(24)
        self.scores = []
        self.refresh_scores()
    
    def refresh_scores(self):
        """
        Actualizar lista de puntuaciones
        """
        self.scores = self.database.get_top_scores(10)
    
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
        Dibujar el ranking
        """
        self.screen.fill(BLACK)
        
        # Título
        title = self.font_large.render("TOP 10 PUNTUACIONES", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)
        
        # Encabezados
        header_y = 120
        headers = ["#", "Nombre", "Puntuacion", "Nivel"]
        header_x_positions = [250, 300, 550, 900]
        
        for i, header in enumerate(headers):
            header_text = self.font_medium.render(header, True, GREEN)
            self.screen.blit(header_text, (header_x_positions[i], header_y))
        
        # Lista de puntuaciones
        if not self.scores:
            no_scores = self.font_medium.render("No hay puntuaciones aun", True, WHITE)
            no_scores_rect = no_scores.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(no_scores, no_scores_rect)
        else:
            start_y = 180
            for idx, (name, score, level) in enumerate(self.scores, 1):
                y_pos = start_y + (idx - 1) * 40
                
                # Número de posición
                pos_text = self.font_small.render(str(idx), True, YELLOW)
                self.screen.blit(pos_text, (header_x_positions[0], y_pos))
                
                # Nombre
                name_text = self.font_small.render(name[:15], True, WHITE)
                self.screen.blit(name_text, (header_x_positions[1], y_pos))
                
                # Puntuación
                score_text = self.font_small.render(str(score), True, WHITE)
                self.screen.blit(score_text, (header_x_positions[2], y_pos))
                
                # Nivel
                level_text = self.font_small.render(str(level), True, WHITE)
                self.screen.blit(level_text, (header_x_positions[3], y_pos))
        
        # Instrucciones
        instruction = self.font_small.render("Presiona ESC o ENTER para volver", True, WHITE)
        instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(instruction, instruction_rect)

