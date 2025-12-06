import pygame
from ..ui import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, load_font

class CreditsScene:
    def __init__(self, screen):
        self.screen = screen
        
        # Cargar fuente personalizada usando el sistema del juego
        self.font = load_font(28)
        
        self.credits = []
        self.scroll_y = screen.get_height()
        self.active = False
        self.finished = False
        self.scroll_speed = 50  # pixeles por segundo

    def start(self, credits_lines):
        """Iniciar créditos con lista de líneas (cada elemento puede ser multilínea)."""
        # aceptar string o lista
        if isinstance(credits_lines, str):
            lines = credits_lines.splitlines()
        else:
            # aplanar lista y separar líneas por salto de línea
            lines = []
            for item in credits_lines:
                lines += [l for l in str(item).splitlines() if l.strip() != ""]
        self.credits = lines
        self.scroll_y = self.screen.get_height()
        self.active = True
        self.finished = False

    def handle_event(self, event):
        """Llamar desde el loop de eventos. Cualquier tecla o botón termina créditos."""
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            if self.active:
                # si está activo, cualquier tecla salta/termina créditos
                self.finished = True
                self.active = False
                return 'menu'
        return None

    def update(self, dt):
        """dt en segundos."""
        if not self.active or self.finished:
            return
        self.scroll_y -= self.scroll_speed * dt
        # marcar terminado cuando todo haya pasado arriba
        total_height = len(self.credits) * (self.font.get_linesize())
        if self.scroll_y + total_height < 0:
            self.finished = True
            self.active = False
            # limpiar líneas para que no se reinicien con una tecla en el menú
            self.credits = []

    def draw(self):
        if not self.active:
            return
        self.screen.fill(BLACK)
        
        # Centrar texto horizontalmente
        for i, line in enumerate(self.credits):
            text = self.font.render(line, True, WHITE)
            text_rect = text.get_rect()
            x = (SCREEN_WIDTH - text_rect.width) // 2
            y = int(self.scroll_y + i * (self.font.get_linesize() + 10))
            self.screen.blit(text, (x, y))
        
        # Instrucción para saltar
        if self.active:
            skip_font = load_font(20)
            skip_text = skip_font.render("Presiona cualquier tecla para volver al menu", True, WHITE)
            skip_rect = skip_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
            self.screen.blit(skip_text, skip_rect)

    def is_finished(self):
        return self.finished