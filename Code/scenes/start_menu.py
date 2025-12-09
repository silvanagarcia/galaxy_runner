"""
Escena del menú de inicio
"""

import pygame
import os
from UI.ui import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GREEN, load_font
from constants.config import get_image_path

class StartMenuScene:
    def __init__(self, screen: pygame.Surface, audio_manager=None):
        self.screen = screen
        self.audio_manager = audio_manager
        
        # Estado de la pantalla: 'screen1' o 'screen2'
        self.current_screen = 'screen1'
        
        # Cargar imágenes de las pantallas
        self.screen1_image = None
        self.screen2_image = None
        
        # Intentar cargar las imágenes personalizadas
        try:
            screen1_path = get_image_path('menu_screen1.png')
            if os.path.exists(screen1_path):
                img = pygame.image.load(screen1_path).convert_alpha()
                self.screen1_image = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            else:
                print(f"Imagen no encontrada: {screen1_path}")
        except Exception as e:
            print(f"Error al cargar menu_screen1.png: {e}")
        
        try:
            screen2_path = get_image_path('menu_screen2.png')
            if os.path.exists(screen2_path):
                img = pygame.image.load(screen2_path).convert_alpha()
                self.screen2_image = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            else:
                print(f"Imagen no encontrada: {screen2_path}")
        except Exception as e:
            print(f"Error al cargar menu_screen2.png: {e}")
        
    def handle_event(self, event: pygame.event.Event) -> str:
        """
        Manejar eventos según la pantalla actual
        Retorna:
        - 'start': para iniciar el juego (solo en screen2)
        - 'ranking': para ver el ranking (solo en screen1)
        - 'next_screen': para avanzar a la siguiente pantalla (solo en screen1)
        """
        if event.type == pygame.KEYDOWN:
            if self.current_screen == 'screen1':
                # Primera pantalla: ENTER avanza, R va al ranking
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if self.audio_manager:
                        self.audio_manager.play_enter_key()
                    self.current_screen = 'screen2'
                    return 'next_screen'
                elif event.key == pygame.K_r:
                    return 'ranking'
            elif self.current_screen == 'screen2':
                # Segunda pantalla: solo ENTER inicia el juego
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if self.audio_manager:
                        self.audio_manager.play_enter_key()
                    return 'start'
        return None
    
    def reset_to_first_screen(self):
        """Reiniciar a la primera pantalla"""
        self.current_screen = 'screen1'
    
    def draw(self):
        """
        Dibujar la pantalla actual
        """
        if self.current_screen == 'screen1':
            # Dibujar primera pantalla
            if self.screen1_image:
                self.screen.blit(self.screen1_image, (0, 0))
            else:
                # Fallback si no hay imagen
                self.screen.fill(BLACK)
                font = load_font(48)
                text = font.render("Pantalla 1 - Presiona ENTER para continuar o R para ranking", True, WHITE)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(text, text_rect)
        elif self.current_screen == 'screen2':
            # Dibujar segunda pantalla
            if self.screen2_image:
                self.screen.blit(self.screen2_image, (0, 0))
            else:
                # Fallback si no hay imagen
                self.screen.fill(BLACK)
                font = load_font(48)
                text = font.render("Pantalla 2 - Presiona ENTER para comenzar", True, WHITE)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(text, text_rect)

