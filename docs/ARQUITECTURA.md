# Arquitectura de Galaxy Runner

Documento técnico. Describe cómo está organizado el código y cómo se
comunican sus partes. Para las reglas de juego (balance, niveles, puntuación)
ver [documento-diseno.md](documento-diseno.md).

---

## 1. Visión general

Galaxy Runner es una aplicación **Pygame** de un solo proceso. Todo el juego
vive en `src/` y se ejecuta con `python src/main.py`.

La organización sigue una separación por capas:

| Capa          | Carpeta            | Responsabilidad                                        |
|---------------|--------------------|--------------------------------------------------------|
| Orquestación  | `src/main.py`      | Bucle principal, ventana, máquina de estados           |
| Escenas       | `src/scenes/`      | Cada pantalla del juego (menú, gameplay, ranking…)     |
| Entidades     | `src/entities/`    | Objetos del juego con lógica y render propios          |
| Servicios     | `src/service/`     | Audio, animación de fondo                              |
| UI            | `src/UI/`          | Carga de fuentes/imágenes, pantallas de introducción   |
| Datos         | `src/db/`          | Acceso a SQLite (`Database`)                           |
| Configuración | `src/constants/`   | Rutas, resolución, colores, constantes de balance      |
| Recursos      | `src/assets/`      | Imágenes y sonidos                                     |

## 2. Bucle principal y ventana

`src/main.py` define la clase `Game`. En `run()`:

```
while running:
    dt = clock.tick(FPS) / 1000.0        # delta time en segundos
    for event in pygame.event.get():
        ...  handle_event(event)          # o QUIT / VIDEORESIZE
    update(dt)
    draw()
    pygame.display.flip()
```

**Resolución virtual + escalado.** El juego siempre dibuja sobre una
`pygame.Surface` de **1280×720**. Al presentar el frame, esa superficie se
escala al tamaño real de la ventana (`present_frame`), que es
**redimensionable** (`pygame.RESIZABLE`), con un mínimo de 640×360. Esto permite
que toda la lógica de posiciones trabaje con coordenadas fijas.

**Delta time.** Todo el movimiento se multiplica por `dt`, así que la velocidad
es independiente de los FPS reales.

## 3. Máquina de estados

`Game.state` es un string. Las transiciones las decide `main.py` a partir del
valor que devuelven `handle_event` / `update` de la escena activa.

```
                 ┌─────────────────────────────┐
                 ▼                             │
   ┌────────┐  start   ┌─────────┐  game_over  │
   │  menu  │────────▶ │ playing │────────────▶│  game_over ──save──▶ menu
   │        │◀──R/Esc─ │         │             │
   │        │          │         │  victory    ▼
   │        │          └─────────┘───────────▶ victory ──save──▶ credits ──▶ menu
   │        │
   │        │──R──▶ ranking ──Esc──▶ menu
   └────────┘
```

Estados: `menu`, `playing`, `game_over`, `victory`, `ranking`, `options`,
`credits`.

## 4. Patrón *Scene*

Todas las escenas comparten la misma interfaz informal:

```python
class AlgunaScene:
    def __init__(self, screen, ...): ...
    def handle_event(self, event) -> str | None:   # devuelve una "acción"
    def update(self, dt): ...                        # (las que lo necesitan)
    def draw(self): ...                              # dibuja sobre `screen`
```

- **`handle_event`** devuelve una *acción* (`'start'`, `'menu'`, `'ranking'`,
  `'save_score'`, …) que `main.py` interpreta para cambiar de estado.
- Todas dibujan sobre la **misma** superficie base (`self.screen`), que les pasa
  `Game` en el constructor.

| Escena                | Nota                                                            |
|-----------------------|----------------------------------------------------------------|
| `StartMenuScene`      | Dos sub-pantallas (`screen1` → `screen2`) sobre imágenes de menú |
| `GameScene`           | El corazón del juego (ver §5)                                   |
| `GameOverScene`       | También se reutiliza para la entrada de nombre en *victory*     |
| `LeaderboardScene`    | Lee el TOP 10 desde `Database`                                  |
| `CreditsScene`        | Texto con scroll vertical; cualquier tecla lo salta             |
| `OptionsScene`        | *Placeholder* ("Opciones en desarrollo")                        |

## 5. GameScene: gameplay

`GameScene` mantiene listas de entidades activas y las procesa cada frame:

```
enemies · projectiles · meteors · explosions · powerups · boss
```

Ciclo por frame (`update(dt)`):

1. Leer teclado (`pygame.key.get_pressed`) y actualizar al `Player`.
2. *Spawn* de enemigos / meteoritos según temporizadores y nivel.
3. `update(dt)` de cada entidad; descartar las que salen de pantalla o mueren.
4. **Detección de colisiones** con `pygame.Rect` (cada entidad expone `.rect`):
   - proyectil del jugador ↔ enemigo / meteorito / jefe
   - proyectil enemigo / jefe ↔ jugador
   - jugador ↔ enemigo / meteorito
   - jugador ↔ power-up
5. Aplicar puntuación, daño, power-ups.
6. Control de nivel: al alcanzar el número de bajas del nivel se invoca al
   **jefe**; al derrotarlo se pasa de nivel. Vencer al Jefe 3 → `'victory'`.
7. Devolver `'game_over'` / `'victory'` / `None`.

**Progresión** (definida en `constants/config.py` y `GameScene`):

| Nivel | Bajas para el jefe | Vida del jefe (`75 + nivel·30`) | Proyectiles del jefe |
|-------|--------------------|-------------------------------|----------------------|
| 1     | 30                 | 105                           | 1                    |
| 2     | 50                 | 135                           | 2 (abanico)          |
| 3     | 80                 | 165                           | 3 (abanico)          |

## 6. Entidades

Cada entidad es una clase independiente en `src/entities/` con la misma forma:
`__init__` (carga su sprite con *fallback* a una figura dibujada), `update(dt)`
y `draw(screen)`. Exponen `.rect` para las colisiones.

| Clase        | Archivo              | Rasgos                                                        |
|--------------|----------------------|--------------------------------------------------------------|
| `Player`     | `player.py`          | Movimiento 8 direcciones, *sprint* (2× por 1 s, enfriamiento 4 s), *cooldown* de disparo, 3 vidas, sprite según dirección |
| `Enemy`      | `enemigos.py`        | Movimiento errático con cambios de dirección aleatorios, confinado a la mitad superior, dispara con *cooldown* aleatorio |
| `Boss`       | `boss.py`            | Rebote horizontal, barra de vida, disparo en abanico según nivel |
| `Meteor`     | `meteorito.py`       | Trayectoria rectilínea + rotación                             |
| `Projectile` | `proyectiles.py`     | Variantes jugador / enemigo / jefe                            |
| `PowerUp`    | `powerup.py`         | Tipos: `health`, `rapid_fire`, `shield`                       |
| `Explosion`  | `explosiones.py`     | Animación por *frames* de círculos de color                   |

## 7. Servicios

### AudioManager (`service/audio_manager.py`)

- Inicializa `pygame.mixer` y **precarga** los efectos (`sfx/`) en un diccionario.
- **Música contextual**: una pista por contexto —
  `menu_music`, `enemies_music`, `boss1_music`, `boss2_music`, `boss3_music`.
  Nunca suenan dos a la vez; las transiciones usan *fade in / fade out*.
- Volúmenes separados: *master*, *sfx*, *music*.
- Si falta un archivo de audio, el juego sigue funcionando **sin sonido**.

### BackgroundAnimation (`service/background_animation.py`)

- Reproduce una secuencia de *frames* (`bg_01.png` … `bg_14.png`) como fondo
  animado. Si no encuentra los archivos, genera *placeholders* con degradado y
  estrellas.
- **Desactivada por defecto** en `GameScene` (`set_animation_enabled(False)`).

## 8. Capa de datos (`db/db_manager.py`)

Clase `Database`, una instancia creada en `Game.__init__`. Cada método abre y
cierra su propia conexión SQLite (operaciones cortas).

- `_create_tables()` — crea `players`, `scores` y el índice si no existen.
- `add_player(name) -> id` — inserta; si el nombre ya existe (UNIQUE), devuelve
  el id existente.
- `add_score(player_id, score, level)`.
- `get_top_scores(limit=10)` — `JOIN` + `ORDER BY score DESC`.
- utilidades: `get_player_scores`, `get_total_players`, `get_total_scores`,
  `clear_all_data`.

Esquema completo en el [README](../README.md#base-de-datos).

## 9. Configuración (`constants/config.py`)

Centraliza:

- **Rutas** derivadas de `BASE_DIR`, con detección de PyInstaller
  (`sys._MEIPASS`) y *helpers* (`get_image_path`, `get_music_path`, …).
- **Pantalla**: `SCREEN_WIDTH`, `SCREEN_HEIGHT`, `FPS`.
- **Colores** con nombre.
- **Balance**: velocidades, vidas, límites de *spawn*, tabla de puntos.

> ⚠️ **Deuda técnica conocida:** `UI/ui.py` **redefine** varias de estas
> constantes (resolución, colores, puntos). Hoy conviven dos fuentes de verdad;
> unificarlas está en el roadmap.

## 10. Empaquetado

`build/GalaxyRunner.spec` + `build/build.bat` generan un ejecutable de escritorio
con **PyInstaller** (modo `--onedir --windowed`). Incluyen los `assets/` y la
base de datos como *datas*.

> Estos scripts todavía referencian la estructura anterior (`Code/`) y deben
> actualizarse a `src/`.

## 11. Flujo de trabajo con Git

- Repositorio en **GitHub**.
- Desarrollo en **ramas de característica** que se integran a `main` mediante
  **Pull Requests** (ver historial: *merge* de `ultima_version` vía PR #1).
- Artefactos de *build* y base de datos **fuera del control de versiones**
  (`.gitignore`).
