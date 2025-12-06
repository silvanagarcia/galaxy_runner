<<<<<<< Updated upstream


GALAXY RUNNER

Space Shooter 2D inspirado en Space Invaders, desarrollado con Pygame y SQLite.

Caracteristicas
- 3 nivles con dificultad progresiva
- Sistema de jefes (uno por nivel)
- Enemigos con patrones de movimiento
- Meteoritos
- Sistema de power-ups (vida, disparo rápido, escudo)
- Sistema de puntuación con base de datos SQLite
- Ranking TOP 10
- Sistema de vidas

Instalación

1 Instalar dependencias:

pip install -r requirements.txt


2 Ejecutar el juego:

python main.py


Controles

- Flechas o WASD: Mover nave
- ESPACIO: Disparar
- R: Ver ranking
- ESC: Salir/Menú

Estructura del Proyecto


GALAXY-RUNNER
── main.py              # Punto de entrada
── game.py              # Lógica principal del juego
── config.py            # Configuración
── database.py          # Sistema de base de datos
── entities:            # Entidades del juego
   ├── player.py
   ├── enemy.py
   ├── boss.py
   ├── projectile.py
   ├── meteor.py
   ├── explosion.py
   └── powerup.py
── screens:             # Pantallas
    ├── menu.py
    ├── game_over.py
    └── ranking.py
    
=======


GALAXY RUNNER

Space Shooter 2D inspirado en Space Invaders, desarrollado con Pygame y SQLite.

Caracteristicas
- 3 nivles con dificultad progresiva
- Sistema de jefes (uno por nivel)
- Enemigos con patrones de movimiento
- Meteoritos
- Sistema de power-ups (vida, disparo rápido, escudo)
- Sistema de puntuación con base de datos SQLite
- Ranking TOP 10
- Sistema de vidas

Instalación

1 Instalar dependencias:

pip install -r requirements.txt


2 Ejecutar el juego:

python main.py


Controles

- Flechas o WASD: Mover nave
- ESPACIO: Disparar
- R: Ver ranking
- ESC: Salir/Menú

Estructura del Proyecto


GALAXY-RUNNER
── main.py              # Punto de entrada
── game.py              # Lógica principal del juego
── config.py            # Configuración
── database.py          # Sistema de base de datos
── entities:            # Entidades del juego
   ├── player.py
   ├── enemy.py
   ├── boss.py
   ├── projectile.py
   ├── meteor.py
   ├── explosion.py
   └── powerup.py
── screens:             # Pantallas
    ├── menu.py
    ├── game_over.py
    └── ranking.py
    
>>>>>>> Stashed changes
Esta es una demo base funcional. Los gráficos y sonidos son temporales (formas básicas y colores). El diseño visual y soundtrack deben agregarse posteriormente.