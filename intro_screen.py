### Sistema de Pantallas de Introducción - Galaxy Runner

import pygame
import os
from typing import Optional
from .ui import load_font

class IntroScreen:
    def __init__(self, screen_width: int, screen_height: int):
        """Inicializar sistema de pantallas de introducción"""
        # Inicializar pygame.font si no está inicializado
        if not pygame.get_init():
            pygame.init()
        if not pygame.font.get_init():
            pygame.font.init()
            
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Estado de la pantalla de introducción
        self.active = False
        self.current_intro = None
        self.timer = 0.0
        self.duration = 4.0  # 4 segundos por pantalla
        
        # Imagen actual
        self.current_image = None
        self.image_loaded = False
        
        # Rutas de imágenes de introducción
        self.intro_images = {
            # Introducciones de esbirros (antes de cada nivel)
            'enemies_level1': 'intros/enemies_level1_intro.png',
            'enemies_level2': 'intros/enemies_level2_intro.png', 
            'enemies_level3': 'intros/enemies_level3_intro.png',
            
            # Introducciones de jefes (antes de cada jefe)
            'boss1': 'intros/boss1_intro.png',
            'boss2': 'intros/boss2_intro.png',
            'boss3': 'intros/boss3_intro.png'
        }
        
        # Cargar imágenes
        self.loaded_images = {}
        self.load_intro_images()
    
    def load_intro_images(self):
        """Cargar todas las imágenes de introducción"""
        from .paths import RES_DIR
        
        print("Cargando imágenes de introducción...")
        
        for intro_name, image_path in self.intro_images.items():
            full_path = os.path.join(RES_DIR, image_path)
            
            try:
                if os.path.exists(full_path):
                    # Cargar y escalar imagen
                    image = pygame.image.load(full_path)
                    scaled_image = pygame.transform.scale(image, (self.screen_width, self.screen_height))
                    self.loaded_images[intro_name] = scaled_image
                    print(f"Imagen de introducción cargada: {intro_name}")
                else:
                    # Crear imagen placeholder si no existe
                    placeholder = self.create_placeholder_image(intro_name)
                    self.loaded_images[intro_name] = placeholder
                    print(f"Imagen de introducción no encontrada, usando placeholder: {full_path}")
            except Exception as e:
                # Crear imagen placeholder en caso de error
                placeholder = self.create_placeholder_image(intro_name)
                self.loaded_images[intro_name] = placeholder
                print(f"Error al cargar imagen {intro_name}: {e}")
    
    def create_placeholder_image(self, intro_name: str) -> pygame.Surface:
        """Crear imagen placeholder para introducciones"""
        surface = pygame.Surface((self.screen_width, self.screen_height))
        
        # Colores según el tipo de introducción
        if 'enemies' in intro_name:
            # Gradiente rojo para esbirros
            color1 = (40, 0, 0)    # Rojo oscuro
            color2 = (120, 20, 20) # Rojo medio
            text_color = (255, 100, 100)
            
            if 'level1' in intro_name:
                title = "NIVEL 1 - ESBIRROS"
                subtitle = "Preparate para el combate"
            elif 'level2' in intro_name:
                title = "NIVEL 2 - ESBIRROS"
                subtitle = "La batalla se intensifica"
            else:
                title = "NIVEL 3 - ESBIRROS"
                subtitle = "Combate final de esbirros"
                
        else:  # boss
            # Gradiente púrpura/dorado para jefes
            color1 = (20, 0, 40)   # Púrpura oscuro
            color2 = (80, 40, 120) # Púrpura medio
            text_color = (255, 200, 100)
            
            if 'boss1' in intro_name:
                title = "JEFE 1"
                subtitle = "El Guardian del Sector"
            elif 'boss2' in intro_name:
                title = "JEFE 2"
                subtitle = "El Comandante de la Flota"
            else:
                title = "JEFE 3"
                subtitle = "El Emperador Galactico"
        
        # Crear gradiente vertical
        for y in range(self.screen_height):
            ratio = y / self.screen_height
            r = int(color1[0] + (color2[0] - color1[0]) * ratio)
            g = int(color1[1] + (color2[1] - color1[1]) * ratio)
            b = int(color1[2] + (color2[2] - color1[2]) * ratio)
            pygame.draw.line(surface, (r, g, b), (0, y), (self.screen_width, y))
        
        # Agregar estrellas de fondo
        import random
        for _ in range(100):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            brightness = random.randint(100, 255)
            pygame.draw.circle(surface, (brightness, brightness, brightness), (x, y), 1)
        
        # Agregar texto usando la fuente del juego
        try:
            # Título principal
            font_large = load_font(72)
            title_surface = font_large.render(title, True, text_color)
            title_rect = title_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
            surface.blit(title_surface, title_rect)
            
            # Subtítulo
            font_medium = load_font(36)
            subtitle_surface = font_medium.render(subtitle, True, text_color)
            subtitle_rect = subtitle_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 20))
            surface.blit(subtitle_surface, subtitle_rect)
            
            # Texto de preparación
            font_small = load_font(24)
            prep_text = "Preparandose para el combate..."
            prep_surface = font_small.render(prep_text, True, (200, 200, 200))
            prep_rect = prep_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 80))
            surface.blit(prep_surface, prep_rect)
            
        except Exception as e:
            # Si falla la carga de fuentes, usar fuente por defecto
            print(f"Error al cargar fuente en intro: {e}")
            font = pygame.font.Font(None, 48)
            text_surface = font.render(title, True, text_color)
            text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            surface.blit(text_surface, text_rect)
        
        return surface
    
    def start_intro(self, intro_type: str) -> bool:
        """Iniciar una pantalla de introducción"""
        if intro_type not in self.intro_images:
            print(f"Tipo de introducción no válido: {intro_type}")
            return False
        
        self.active = True
        self.current_intro = intro_type
        self.timer = 0.0
        self.current_image = self.loaded_images.get(intro_type)
        self.image_loaded = self.current_image is not None
        
        print(f"Iniciando introducción: {intro_type}")
        return True
    
    def update(self, dt: float) -> bool:
        """Actualizar pantalla de introducción. Retorna True si sigue activa"""
        if not self.active:
            return False
        
        self.timer += dt
        
        # Verificar si la introducción ha terminado
        if self.timer >= self.duration:
            self.active = False
            self.current_intro = None
            self.current_image = None
            print("Introduccion completada")
            return False
        
        return True
    
    def draw(self, screen: pygame.Surface):
        """Dibujar la pantalla de introducción"""
        if not self.active or not self.current_image:
            return
        
        # Dibujar imagen de introducción
        screen.blit(self.current_image, (0, 0))
        
        # Agregar barra de progreso opcional
        progress_width = int((self.timer / self.duration) * (self.screen_width - 100))
        progress_rect = pygame.Rect(50, self.screen_height - 30, progress_width, 10)
        pygame.draw.rect(screen, (100, 200, 255), progress_rect)
        
        # Marco de la barra de progreso
        frame_rect = pygame.Rect(50, self.screen_height - 30, self.screen_width - 100, 10)
        pygame.draw.rect(screen, (255, 255, 255), frame_rect, 2)
    
    def is_active(self) -> bool:
        """Verificar si hay una introducción activa"""
        return self.active
    
    def get_current_intro(self) -> Optional[str]:
        """Obtener el tipo de introducción actual"""
        return self.current_intro if self.active else None
    
    def skip_intro(self):
        """Saltar la introducción actual"""
        if self.active:
            self.active = False
            self.current_intro = None
            self.current_image = None
            print("Introducción saltada")
    
    def get_remaining_time(self) -> float:
        """Obtener tiempo restante de la introducción"""
        if not self.active:
            return 0.0
        return max(0.0, self.duration - self.timer)
    
    def reload_images(self):
        """Recargar todas las imágenes de introducción"""
        self.loaded_images.clear()
        self.load_intro_images()
        print("Imágenes de introducción recargadas")
