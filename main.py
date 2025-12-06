"""
Galaxy Runner - Punto de entrada principal
"""

import pygame
import sys
import os

# Agregar directorio padre a la ruta para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from galaxy_runner.db import Database
from galaxy_runner.paths import DB_PATH
from galaxy_runner.ui import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from galaxy_runner.scenes import StartMenuScene, GameScene, LeaderboardScene, OptionsScene, CreditsScene
from galaxy_runner.scenes.game_over_scene import GameOverScene
from galaxy_runner.audio_manager import AudioManager


class Game:
    def __init__(self):
        pygame.init()
        
        # Configuración de pantalla (ventana redimensionable)
        self.display_flags = pygame.RESIZABLE | pygame.DOUBLEBUF
        self.window_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.display_surface = pygame.display.set_mode(self.window_size, self.display_flags)
        pygame.display.set_caption("Galaxy Runner")
        # Superficie base donde se dibuja el juego (mantiene la resolución virtual)
        self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
        self.clock = pygame.time.Clock()
        
        # Base de datos
        self.database = Database(DB_PATH)
        
        # Audio Manager
        self.audio_manager = AudioManager()
        
        # Estado del juego
        self.state = 'menu'  # menu, playing, game_over, victory, ranking, options, credits
        
        # Escenas (todas dibujan sobre la superficie base)
        self.start_menu = StartMenuScene(self.screen, self.audio_manager)
        self.game_scene = GameScene(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT, self.audio_manager)
        self.game_over_scene = GameOverScene(self.screen)
        self.leaderboard_scene = LeaderboardScene(self.screen, self.database)
        self.options_scene = OptionsScene(self.screen)
        self.credits_scene = CreditsScene(self.screen)
        
        # Reproducir música del menú al inicio
        self.audio_manager.play_menu_music()
        
        # Créditos del juego
        self.setup_credits()
        
        # Fondo del menú
        self.menu_bg = None
        try:
            from .paths import get_image_path
            img_path = get_image_path('main_menu_bg.png')
            if os.path.exists(img_path):
                self.menu_bg = pygame.transform.scale(
                    pygame.image.load(img_path).convert_alpha(),
                    (SCREEN_WIDTH, SCREEN_HEIGHT)
                )
        except Exception as e:
            print(f"No se pudo cargar la imagen de fondo del menú: {e}")
    
    def setup_credits(self):
        """Configurar el contenido de los créditos"""
        credits_lines = [
                "",
                "Has ganado el juego!!",
                "Nombre: " + self.game_over_scene.player_name,
                "Puntuacion: " + str(self.game_scene.get_score()),
                "Nivel: " + str(self.game_scene.get_level()),
                "",
                "Director del juego: Silvana Garcia",
                "Programadores: Martin Lopez - Ivar Sosa",
                "",
                "Agradecimientos especiales: ITES",
                "Profesores de desarrollo de software.",
                "",
                "MUCHAS GRACIAS POR JUGAR GALAXY RUNNER 2025!"
            ]
        self.credits_scene.start(credits_lines)
    
    def handle_event(self, event: pygame.event.Event):
        """Manejar eventos"""
        if self.state == 'menu':
            action = self.start_menu.handle_event(event)
            if action == 'start':
                # Iniciar juego desde la segunda pantalla
                self.game_scene.reset_game()
                self.state = 'playing'
                self.audio_manager.play_enemies_music()
                self.start_menu.reset_to_first_screen()  # Resetear para la próxima vez
            elif action == 'ranking':
                # Ver ranking desde la primera pantalla
                self.leaderboard_scene.refresh_scores()
                self.state = 'ranking'
            elif action == 'next_screen':
                # Avanzar a la segunda pantalla (ya se maneja internamente)
                pass
        
        elif self.state == 'playing':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.audio_manager.stop_music()
                    self.audio_manager.play_menu_music()
                    self.start_menu.reset_to_first_screen()
                    self.state = 'menu'
                elif event.key == pygame.K_r:
                    self.leaderboard_scene.refresh_scores()
                    self.state = 'ranking'
            # La escena del juego maneja su propia actualización
        
        elif self.state == 'game_over':
            action = self.game_over_scene.handle_event(event)
            if action == 'save_score':
                player_name = self.game_over_scene.get_player_name()
                if player_name:
                    player_id = self.database.add_player(player_name)
                    self.database.add_score(
                        player_id, 
                        self.game_over_scene.score, 
                        self.game_over_scene.level
                    )
                    self.leaderboard_scene.refresh_scores()
            elif action == 'menu':
                self.game_over_scene.reset()
                self.audio_manager.play_menu_music()
                self.start_menu.reset_to_first_screen()  # Resetear a la primera pantalla
                self.state = 'menu'
        
        elif self.state == 'victory':
            action = self.game_over_scene.handle_event(event)
            if action == 'save_score':
                player_name = self.game_over_scene.get_player_name()
                if player_name:
                    player_id = self.database.add_player(player_name)
                    self.database.add_score(
                        player_id,
                        self.game_over_scene.score,
                        self.game_over_scene.level
                    )
                    self.leaderboard_scene.refresh_scores()
                    # Después de guardar, mostrar créditos automáticamente
                    # Detener cualquier música/sonido antes de mostrar créditos
                    self.audio_manager.stop_music()
                    self.audio_manager.stop_all_sounds()
                    self.setup_credits()
                    self.state = 'credits'
            # No permitir volver al menú desde victoria hasta ver créditos
        
        elif self.state == 'credits':
            action = self.credits_scene.handle_event(event)
            if action == 'menu':
                # Detener toda la música y sonidos antes de volver al menú
                self.audio_manager.stop_music()
                self.audio_manager.stop_all_sounds()
                self.audio_manager.play_menu_music()
                self.game_over_scene.reset()
                self.state = 'menu'
        
        elif self.state == 'ranking':
            action = self.leaderboard_scene.handle_event(event)
            if action == 'menu':
                self.start_menu.reset_to_first_screen()
                self.state = 'menu'
        
        elif self.state == 'options':
            action = self.options_scene.handle_event(event)
            if action == 'menu':
                self.start_menu.reset_to_first_screen()
                self.state = 'menu'
    
    def update(self, dt: float):
        """Actualizar estado del juego"""
        if self.state == 'playing':
            result = self.game_scene.update(dt)
            if result == 'game_over':
                self.audio_manager.stop_music()
                self.audio_manager.play_game_over()
                self.game_over_scene.set_score(
                    self.game_scene.get_score(),
                    self.game_scene.get_level()
                )
                self.game_over_scene.reset()
                self.state = 'game_over'
            elif result == 'victory':
                self.audio_manager.stop_music()
                self.audio_manager.play_victory()
                self.game_over_scene.set_score(
                    self.game_scene.get_score(),
                    self.game_scene.get_level()
                )
                self.game_over_scene.reset()
                self.state = 'victory'
        elif self.state == 'credits':
            self.credits_scene.update(dt)
            if self.credits_scene.is_finished():
                # Detener toda la música y sonidos antes de volver al menú
                self.audio_manager.stop_music()
                self.audio_manager.stop_all_sounds()
                self.audio_manager.play_menu_music()
                self.game_over_scene.reset()
                self.start_menu.reset_to_first_screen()
                self.state = 'menu'
    
    def draw(self):
        """Dibujar estado actual"""
        self.screen.fill((0, 0, 0))
        if self.state == 'menu':
            if self.menu_bg:
                self.screen.blit(self.menu_bg, (0, 0))
            self.start_menu.draw()
        elif self.state == 'playing':
            self.game_scene.draw()
        elif self.state == 'game_over':
            self.game_over_scene.draw()
        elif self.state == 'victory':
            self.draw_victory()
        elif self.state == 'ranking':
            self.leaderboard_scene.draw()
        elif self.state == 'options':
            self.options_scene.draw()
        elif self.state == 'credits':
            self.credits_scene.draw()
        self.present_frame()

    def present_frame(self):
        """Escalar y mostrar la superficie base en la ventana actual"""
        window_width, window_height = self.display_surface.get_size()
        base_width, base_height = self.screen.get_size()
        if (window_width, window_height) == (base_width, base_height):
            self.display_surface.blit(self.screen, (0, 0))
        else:
            scaled_surface = pygame.transform.smoothscale(self.screen, (window_width, window_height))
            self.display_surface.blit(scaled_surface, (0, 0))
    
    def draw_victory(self):
        """Dibujar pantalla de victoria"""
        self.screen.fill((0, 0, 0))
        
        from galaxy_runner.ui import load_font
        font_large = load_font(72)
        font_medium = load_font(48)
        font_small = load_font(24)
        
        # Título de victoria
        title = font_large.render("VICTORIA!", True, (0, 255, 0))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))
        self.screen.blit(title, title_rect)
        
        # Mensaje
        msg = font_medium.render("Has completado el juego!", True, (255, 255, 255))
        msg_rect = msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
        self.screen.blit(msg, msg_rect)
        
        # Puntuación
        score_text = font_medium.render(
            f"Puntuacion Final: {self.game_over_scene.score}", 
            True, (255, 255, 0)
        )
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(score_text, score_rect)
        
        # Entrada de nombre (igual que game_over)
        if self.game_over_scene.entering_name:
            name_prompt = font_small.render(
                "Ingresa tu nombre para guardar tu record:", 
                True, (255, 255, 255)
            )
            name_prompt_rect = name_prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(name_prompt, name_prompt_rect)
            
            name_display = font_medium.render(
                self.game_over_scene.player_name + "_", 
                True, (0, 255, 0)
            )
            name_display_rect = name_display.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
            self.screen.blit(name_display, name_display_rect)
            
            enter_text = font_small.render("Presiona ENTER para continuar", True, (255, 255, 255))
            enter_rect = enter_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
            self.screen.blit(enter_text, enter_rect)
        else:
            saved_text = font_small.render("Puntuacion guardada!", True, (0, 255, 0))
            saved_rect = saved_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(saved_text, saved_rect)
            
            continue_text = font_small.render("Mostrando creditos...", True, (255, 255, 255))
            continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
            self.screen.blit(continue_text, continue_rect)
    
    def run(self):
        """Bucle principal del juego"""
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.handle_window_resize(event)
                else:
                    self.handle_event(event)
            
            self.update(dt)
            self.draw()
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

    def handle_window_resize(self, event: pygame.event.Event):
        """Actualizar la superficie de la ventana al redimensionar/maximizar"""
        min_width, min_height = 640, 360
        new_width = max(event.w, min_width)
        new_height = max(event.h, min_height)
        if (new_width, new_height) != self.window_size:
            self.window_size = (new_width, new_height)
            self.display_surface = pygame.display.set_mode(self.window_size, self.display_flags)


def main():
    """Punto de entrada"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()

