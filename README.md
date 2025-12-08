

GALAXY RUNNER


Galaxy Runner es un space shooter 2D inspirado en el conocido Space Invaders de los años 80s, con un estilo pixel art y mecánicas sencillas de movimiento, disparo de proyectiles, colisiones, y puntuación. El juego esta Desarrollado en Python, utilizando la librería Pygame para el motor gráfico y SQLite para el registro de puntuaciones.

Descripción General:
El jugador controla una nave con el objetivo de eliminar oleadas de enemigos mientras esquiva proyectiles o meteoritos y acumula puntos. El videojuego cuenta con 3 niveles distintos en donde la dificultad del entorno pone a prueba al jugador a medida que avanza y completa cada parte. La jugabilidad es sencilla pero desafiante.


Caracteristicas Principales:

- Tres escenarios con ambientaciones distintas.

- 3 niveles con dificultad progresiva:
	• Nivel 1: Juego base + Jefe.
	• Nivel 2: Velocidad aumentada + Jefe.
	• Nivel 3: Máxima dificultad + Jefe final.

- Sistema de jefes (uno por nivel, en total 3)
- Enemigos con patrones de movimiento
- Objetos con colisión (Meteoritos)
- Sistema de power-ups (vida, disparo rápido, escudo)
- Sistema de puntuación con base de datos SQLite
- Ranking TOP 10
- Sistema de vidas
- Soundtrack y efectos de sonido para una ambientacion mas completa.




Instalar dependencias:

pip install -r requirements.txt



Ejecutar el juego(2 OPCIONES):

python main.py (CONSOLA DEL EDITOR)
Ejecutar el acceso directo GalaxyRunner dentro de la carpeta principal


Controles

- Flechas o WASD: Mover nave
- teclas: Shift Izq para un movimiento rapido de la nave
- ESPACIO: Disparar
- R: Ver ranking
- ESC: Salir/Menú



Estructura del Proyecto:

galaxy_runner/ 
│ 
├── Code/ 
│   │ 
│   ├──__init__.py
│   │ 
│   ├── main.py 
│   │ 
│   ├── entities/ 
│   │   └── (Clases de cada entidad, con sus metodos y atributos) 
│   ├── UI/ 
│   │   └── (archivos relacionados a interfaz de usuario) 
│   │ 
│   ├── assets/ 
│   │   ├── images/ 
│   │   ├── sounds/ 
│   │   └── backgrounds/ 
│   │ 
│   ├── constants/ 
│   │   └── config.py 
│   │ 
│   ├── db/ 
│   │   ├── db_manager.py 
│   │   └── galaxy.db 
│   │ 
│   ├── repository/ 
│   │   └── (archivos para lectura/escritura de datos) 
│   │ 
│   ├── scenes/ 
│   │   └── (pantallas del juego: intro, menú, gameplay, game over) │   │ 
│   └── service/ 
│       └── (servicios como audio, carga de recursos, animaciones) 
│ 
├── res/ 
│   ├── logo aplicacion.ico
│   ├── banner.jpg 
│   └── (otras imágenes o recursos gráficos para documentación, portada del juego, etc.) 
│ 
├── dist/
│   ├── GalaxyRunner/ 
│   │	 └──_internal/
│   │	 └──GalaxyRunner.exe
│   │
│   └── (Empaquetado del codigo para poder ejecutarlo en cualquier maquina) 
│
├── GalaxyRunner(Acceso Directo)
│ 
├── build.bat
│ 
├── error.log
│ 
├── GalaxyRunner.spec
│
├── requirements.txt
|
└── README.md

