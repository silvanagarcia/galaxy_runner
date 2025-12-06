### Audio Manager - Sistema de sonidos para Galaxy Runner

import pygame
import os
from typing import Dict, Optional

class AudioManager:
    def __init__(self):
        """Inicializar el sistema de audio"""
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Diccionario para almacenar los sonidos cargados
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        
        # Configuración de volumen
        self.master_volume = 0.7
        self.sfx_volume = 0.8
        self.music_volume = 0.6
        
        # Sistema de música de fondo
        self.current_music = None
        self.music_playing = False
        self.music_paused = False
        
        # Rutas de música de fondo
        self.music_paths = {
            'menu_music': 'music/menu_music.mp3',
            'enemies_music': 'music/enemies_music.mp3',
            'boss1_music': 'music/boss1_music.mp3',
            'boss2_music': 'music/boss2_music.mp3',
            'boss3_music': 'music/boss3_music.mp3'
        }
        
        # Rutas de archivos de sonido
        self.sound_paths = {
            # Pantallas y menús
            'enter_key': 'sounds/enter_key.mp3',
            
            # Disparos
            'player_shoot': 'sounds/player_shoot.mp3',
            'enemy_shoot': 'sounds/enemy_shoot.mp3',
            'boss_shoot': 'sounds/boss_shoot.mp3',
            
            # Muerte de enemigos
            'boss_death': 'sounds/boss_death.mp3',
            
            # Power-ups
            'powerup_health': 'sounds/powerup_health.mp3',
            'powerup_rapid_fire': 'sounds/powerup_rapid_fire.mp3',
            'powerup_shield': 'sounds/powerup_shield.mp3',
            
            # Colisiones y daño
            'player_hit': 'sounds/player_hit.mp3',
            'collision': 'sounds/collision.mp3',
            
            # Estados del juego
            'game_over': 'sounds/game_over.mp3',
            'victory': 'sounds/victory.mp3'
        }
        
        # Cargar sonidos
        self.load_sounds()
        
        # Cargar música
        self.load_music()
    
    def load_sounds(self):
        """Cargar todos los archivos de sonido"""
        from .paths import SFX_DIR
        
        for sound_name, sound_path in self.sound_paths.items():
            full_path = os.path.join(SFX_DIR, sound_path)
            
            try:
                if os.path.exists(full_path):
                    sound = pygame.mixer.Sound(full_path)
                    sound.set_volume(self.sfx_volume * self.master_volume)
                    self.sounds[sound_name] = sound
                    print(f"Sonido cargado: {sound_name}")
                else:
                    print(f"Archivo de sonido no encontrado: {full_path}")
            except Exception as e:
                print(f"Error al cargar sonido {sound_name}: {e}")
    
    def load_music(self):
        """Verificar que existan los archivos de música"""
        from .paths import SFX_DIR
        
        print("Verificando archivos de música...")
        for music_name, music_path in self.music_paths.items():
            full_path = os.path.join(SFX_DIR, music_path)
            if os.path.exists(full_path):
                print(f"Música encontrada: {music_name}")
            else:
                print(f"Archivo de música no encontrado: {full_path}")
    
    def play_music(self, music_name: str, loops: int = -1, fade_in_ms: int = 1000):
        """Reproducir música de fondo"""
        if music_name not in self.music_paths:
            print(f"Música no encontrada: {music_name}")
            return
        
        from .paths import SFX_DIR
        full_path = os.path.join(SFX_DIR, self.music_paths[music_name])
        
        if not os.path.exists(full_path):
            print(f"Archivo de música no encontrado: {full_path}")
            return
        
        try:
            # Detener música actual si está sonando
            if self.music_playing:
                pygame.mixer.music.fadeout(500)  # Fade out en 500ms
            
            # Cargar y reproducir nueva música
            pygame.mixer.music.load(full_path)
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
            
            if fade_in_ms > 0:
                pygame.mixer.music.play(loops, fade_ms=fade_in_ms)
            else:
                pygame.mixer.music.play(loops)
            
            self.current_music = music_name
            self.music_playing = True
            self.music_paused = False
            print(f"Reproduciendo música: {music_name}")
            
        except Exception as e:
            print(f"Error al reproducir música {music_name}: {e}")
    
    def stop_music(self, fade_out_ms: int = 1000):
        """Detener música de fondo"""
        if self.music_playing:
            if fade_out_ms > 0:
                pygame.mixer.music.fadeout(fade_out_ms)
            else:
                pygame.mixer.music.stop()
            
            self.current_music = None
            self.music_playing = False
            self.music_paused = False
            print("Música detenida")
    
    def pause_music(self):
        """Pausar música de fondo"""
        if self.music_playing and not self.music_paused:
            pygame.mixer.music.pause()
            self.music_paused = True
            print("Música pausada")
    
    def resume_music(self):
        """Reanudar música de fondo"""
        if self.music_playing and self.music_paused:
            pygame.mixer.music.unpause()
            self.music_paused = False
            print("Música reanudada")
    
    def is_music_playing(self) -> bool:
        """Verificar si hay música reproduciéndose"""
        return self.music_playing and pygame.mixer.music.get_busy()
    
    def get_current_music(self) -> Optional[str]:
        """Obtener el nombre de la música actual"""
        return self.current_music if self.music_playing else None
    
    # Métodos específicos para cada tipo de música
    def play_menu_music(self):
        """Reproducir música del menú"""
        self.play_music('menu_music')
    
    def play_enemies_music(self):
        """Reproducir música durante combate con esbirros"""
        if self.current_music != 'enemies_music':
            self.play_music('enemies_music')
    
    def play_boss1_music(self):
        """Reproducir música del jefe 1"""
        if self.current_music != 'boss1_music':
            self.play_music('boss1_music')
    
    def play_boss2_music(self):
        """Reproducir música del jefe 2"""
        if self.current_music != 'boss2_music':
            self.play_music('boss2_music')
    
    def play_boss3_music(self):
        """Reproducir música del jefe 3"""
        if self.current_music != 'boss3_music':
            self.play_music('boss3_music')

    def play_sound(self, sound_name: str, volume_modifier: float = 1.0):
        """Reproducir un sonido específico"""
        if sound_name in self.sounds:
            sound = self.sounds[sound_name]
            # Crear una copia del sonido para modificar el volumen sin afectar el original
            temp_sound = sound.copy() if hasattr(sound, 'copy') else sound
            current_volume = self.sfx_volume * self.master_volume * volume_modifier
            temp_sound.set_volume(min(1.0, current_volume))
            temp_sound.play()
        else:
            print(f"Sonido no encontrado: {sound_name}")
    
    def play_enter_key(self):
        """Sonido al presionar ENTER"""
        self.play_sound('enter_key')
    
    def play_player_shoot(self):
        """Sonido de disparo del jugador"""
        self.play_sound('player_shoot', 0.6)  # Volumen más bajo para disparos frecuentes
    
    def play_enemy_shoot(self):
        """Sonido de disparo de esbirros"""
        self.play_sound('enemy_shoot', 0.5)
    
    def play_boss_shoot(self):
        """Sonido de disparo de jefes"""
        self.play_sound('boss_shoot', 0.8)
    
    def play_boss_death(self):
        """Sonido cuando muere un jefe"""
        self.play_sound('boss_death')
    
    def play_powerup_health(self):
        """Sonido al recoger power-up de salud"""
        self.play_sound('powerup_health')
    
    def play_powerup_rapid_fire(self):
        """Sonido al recoger power-up de disparo rápido"""
        self.play_sound('powerup_rapid_fire')
    
    def play_powerup_shield(self):
        """Sonido al recoger power-up de escudo"""
        self.play_sound('powerup_shield')
    
    def play_player_hit(self):
        """Sonido cuando el jugador recibe daño"""
        self.play_sound('player_hit')
    
    def play_collision(self):
        """Sonido de colisión general (meteoros, proyectiles)"""
        self.play_sound('collision', 0.7)
    
    def play_game_over(self):
        """Sonido de game over"""
        self.play_sound('game_over')
    
    def play_victory(self):
        """Sonido de victoria"""
        if self.current_music != 'victory':
            self.play_music('victory')
    
    def set_master_volume(self, volume: float):
        """Establecer volumen maestro (0.0 - 1.0)"""
        self.master_volume = max(0.0, min(1.0, volume))
        # Actualizar volumen de todos los sonidos cargados
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume * self.master_volume)
    
    def set_sfx_volume(self, volume: float):
        """Establecer volumen de efectos de sonido (0.0 - 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        # Actualizar volumen de todos los sonidos cargados
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume * self.master_volume)
    
    def stop_all_sounds(self):
        """Detener todos los sonidos"""
        pygame.mixer.stop()
    
    def reload_sounds(self):
        """Recargar todos los sonidos (útil si se agregan nuevos archivos)"""
        self.sounds.clear()
        self.load_sounds()
