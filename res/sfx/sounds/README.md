# Archivos de Sonido para Galaxy Runner

Este directorio contiene todos los efectos de sonido del juego. Coloca tus archivos .mp3 aquí con los nombres exactos especificados.

## Archivos de Sonido Requeridos:

### 🎵 Pantallas y Menús
- **menu_start.mp3** - Sonido al iniciar el juego (primera pantalla)
- **enter_key.mp3** - Sonido al presionar la tecla ENTER

### 🔫 Disparos
- **player_shoot.mp3** - Sonido de disparo del jugador
- **enemy_shoot.mp3** - Sonido de disparo de esbirros
- **boss_shoot.mp3** - Sonido de disparo de jefes

### 💀 Muerte de Enemigos
- **boss_death.mp3** - Sonido cuando muere un jefe

### ⭐ Power-ups
- **powerup_health.mp3** - Sonido al recoger power-up de salud (corazón)
- **powerup_rapid_fire.mp3** - Sonido al recoger power-up de disparo rápido
- **powerup_shield.mp3** - Sonido al recoger power-up de escudo

### 💥 Colisiones y Daño
- **player_hit.mp3** - Sonido cuando el jugador recibe daño
- **collision.mp3** - Sonido de colisión general (meteoros, proyectiles con jugador)

### 🎮 Estados del Juego
- **game_over.mp3** - Sonido de game over
- **victory.mp3** - Sonido de victoria

## Notas:
- Todos los archivos deben estar en formato .mp3
- Los nombres de archivo deben coincidir exactamente con los listados arriba
- Si un archivo no existe, el juego funcionará normalmente pero sin ese sonido específico
- El sistema de audio se inicializa automáticamente al cargar el juego
- Los volúmenes están preconfigurados pero se pueden ajustar en el código

## Configuración de Volumen:
- Volumen maestro: 70%
- Efectos de sonido: 80%
- Los disparos tienen volumen reducido para evitar saturación de audio

¡Simplemente coloca tus archivos .mp3 en este directorio y el juego los cargará automáticamente!
