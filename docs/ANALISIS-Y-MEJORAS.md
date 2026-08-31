# Análisis del repositorio y mejoras propuestas

Revisión del estado del proyecto a la fecha de la reorganización.
El foco es **qué se puede mejorar sin reescribir la lógica del juego**:
estructura, documentación, higiene del repositorio y proceso.

Cada punto lleva una etiqueta de **impacto** (alto / medio / bajo) y de
**esfuerzo** (bajo / medio / alto).

---

## Resumen

| # | Tema | Estado | Impacto | Esfuerzo |
|---|------|--------|---------|----------|
| 1 | Artefactos de build versionados (`dist/`) | ✅ resuelto en la reorg | Alto | Bajo |
| 2 | Historial de Git inflado (~370 MB) | ✅ resuelto en la reorg | Alto | Medio |
| 3 | Base de datos con datos reales versionada | ✅ resuelto en la reorg | Alto | Bajo |
| 4 | `.gitignore` incompleto | ✅ resuelto en la reorg | Alto | Bajo |
| 5 | Copia duplicada de assets (`_internal/`) | ✅ resuelto en la reorg | Medio | Bajo |
| 6 | README desactualizado / incompleto | ✅ resuelto en la reorg | Alto | Medio |
| 7 | Estructura de carpetas poco convencional | ✅ resuelto en la reorg | Medio | Medio |
| 8 | Sin `LICENSE` ni documentación técnica | ✅ resuelto en la reorg | Medio | Bajo |
| 9 | Doble fuente de configuración (`config.py` vs `UI/ui.py`) | ⏳ pendiente | Medio | Medio |
| 10 | Scripts de build (`build/`) desactualizados | ⏳ pendiente | Medio | Medio |
| 11 | Import inconsistente en `background_animation.py` | ✅ corregido (1 línea) | Bajo | Bajo |
| 12 | Nomenclatura mixta español / inglés | ⏳ pendiente | Bajo | Alto |
| 13 | Assets pesados (MP3 de música, ~42 MB) en Git | ⏳ pendiente | Medio | Medio |
| 14 | Sin tests ni integración continua | ⏳ pendiente | Medio | Alto |
| 15 | Pantalla de Opciones incompleta | ⏳ pendiente | Bajo | Medio |
| 16 | Rama `ultima_version` colgada en el remoto | ⏳ pendiente | Bajo | Bajo |
| 17 | Fuente tipográfica ausente del repo | ⏳ pendiente | Bajo | Bajo |

---

## Resuelto en esta reorganización

### 1. `dist/` versionado (112 MB)

El repositorio incluía el build de escritorio completo para Windows:
`GalaxyRunner.exe`, todas las DLLs de SDL2, `python313.dll`, numpy, pygame
compilado. Nada de eso pertenece al control de versiones: se **regenera** con
PyInstaller y depende del sistema operativo.

**Acción:** eliminado del árbol y purgado del historial. `dist/` y `build/`
generados ahora están en `.gitignore`.

### 2. Historial de Git inflado

`.git/` pesaba ~156 MB porque `dist/`, la base de datos, el `.docx` y binarios
varios entraron y salieron del historial varias veces.

**Acción:** historial reescrito con `git filter-repo` para eliminar esos blobs
de todos los commits. El repo pasó a un tamaño acorde al código + los assets
que el juego realmente necesita.

> Consecuencia: `main` recibió un *force-push*. Cualquier clon anterior debe
> volver a clonarse.

### 3. Base de datos versionada con datos reales

`Code/db/galaxy.db` estaba en Git con **nombres de jugadores y puntajes reales**
de partidas de prueba. Además, el código ya la crea sola al arrancar
(`Database._create_tables`), así que versionarla no aportaba nada.

**Acción:** eliminada del árbol y del historial. `*.db` en `.gitignore`.

### 4. `.gitignore` incompleto

Contenía una sola línea (`/galaxy_runner`). Por eso entraron al repo los
`__pycache__/`, el `.exe`, la base de datos y `error.log`.

**Acción:** `.gitignore` nuevo cubriendo Python, PyInstaller, `*.db`, logs y
archivos de sistema operativo / editores.

### 5. Copia duplicada de assets

`Code/assets/images/_internal/galaxy_runner/res/...` y
`Code/assets/sounds/_internal/...` eran una **segunda copia** de todos los
sprites y sonidos (≈48 MB), sobrante de un empaquetado anterior.

**Acción:** eliminada del árbol y del historial.

### 6. README desactualizado

El árbol de directorios del README mencionaba carpetas que no existen
(`backgrounds/`, `banner.jpg`, `fonts/`), el comando de ejecución era incorrecto
(`python main.py` cuando el entrypoint está en `Code/main.py`), no había
capturas y `requirements.txt` solo listaba `pygame`.

**Acción:** README reescrito con instalación real, controles completos, tablas
de balance, esquema de base de datos, estructura verdadera y roadmap.

### 7. Estructura de carpetas

- Carpeta principal llamada `Code/` (poco habitual en Python; lo usual es
  `src/` o el nombre del paquete).
- `res/` en la raíz **y** `Code/assets/` — dos lugares para recursos.
- `GalaxyRunner.spec`, `build.bat` y `error.log` sueltos en la raíz.
- `Code/repository/` era un paquete vacío, nunca importado.
- `Galaxy Runner.docx` (508 KB) suelto en la raíz.

**Acción:** `Code/` → `src/`; scripts de build a `build/`; documentación a
`docs/`; capturas a `docs/screenshots/`; `repository/` eliminado.

### 8. Sin licencia ni documentación técnica

No había `LICENSE`, `CHANGELOG.md`, ni ningún documento que explicara la
arquitectura.

**Acción:** agregados `LICENSE` (MIT), `CHANGELOG.md`, `docs/ARQUITECTURA.md`,
`docs/CREDITOS.md` y `docs/documento-diseno.md`.

### 11. Import inconsistente

`src/service/background_animation.py` era el único módulo que importaba con
`from Code.constants.config import ...` en vez de `from constants.config
import ...`. Al renombrar la carpeta esto se rompía.

**Acción:** corregido a la forma que usan los otros ~20 módulos. Es el único
cambio de código de la reorganización, junto con una ruta de PyInstaller en
`config.py`.

---

## Pendiente — no requiere reescribir la lógica

### 9. Doble fuente de configuración · impacto medio · esfuerzo medio

`src/constants/config.py` y `src/UI/ui.py` **definen las mismas constantes**
(resolución, colores, puntajes, velocidades). Hoy conviven dos "fuentes de
verdad" y es fácil que se desincronicen.

**Propuesta:** dejar `config.py` como única fuente y que `UI/ui.py` re-exporte
desde ahí (`from constants.config import *`), o directamente que los módulos
importen de `constants.config`. Es un cambio mecánico de imports, sin tocar
comportamiento.

### 10. Scripts de build desactualizados · impacto medio · esfuerzo medio

`build/GalaxyRunner.spec` y `build/build.bat` fueron migrados a `src/` pero
siguen teniendo inconsistencias heredadas: referencian `assets/backgrounds` y
`assets/fonts` que no existen, y el manejo de rutas para el ejecutable
congelado (`sys._MEIPASS`) no está alineado con el `.spec`.

**Propuesta:** revisar el flujo de empaquetado de punta a punta en una PC
Windows, validar que el `.exe` encuentra `assets/` y crea la base de datos, y
documentar el resultado.

### 12. Nomenclatura mixta · impacto bajo · esfuerzo alto

Nombres de archivos y clases mezclan idiomas: `enemigos.py` / `proyectiles.py`
/ `meteorito.py` junto a `player.py` / `boss.py`; clases en inglés (`Enemy`,
`Meteor`) en archivos con nombre en español.

**Propuesta:** elegir un idioma (recomendado: inglés para el código, español
para la documentación) y renombrar en un único PR dedicado. Es de bajo riesgo
pero toca muchos imports, por eso el esfuerzo es alto.

### 13. Assets de audio pesados en Git · impacto medio · esfuerzo medio

Los 5 MP3 de música suman ~42 MB y son la mayor parte del peso del repo. Git no
maneja bien archivos binarios grandes que podrían cambiar.

**Propuesta:** mover el audio a **Git LFS**, o publicarlo como un release
adjunto y que un script lo descargue. Mantener los efectos de sonido (son
chicos) en el repo.

### 14. Sin tests ni CI · impacto medio · esfuerzo alto

No hay pruebas automatizadas. La lógica pura (balance, `Database`, cálculo de
ranking, colisiones de `Rect`) es perfectamente testeable sin abrir una
ventana.

**Propuesta:** empezar con `pytest` sobre `Database` y las funciones de
`config.py`, y un workflow de GitHub Actions que corra los tests y un
*smoke test* de importación (`import main` con `SDL_VIDEODRIVER=dummy`).

### 15. Pantalla de Opciones incompleta · impacto bajo · esfuerzo medio

`OptionsScene` solo muestra "Opciones en desarrollo". El `AudioManager` ya
soporta volúmenes separados, así que la escena podría exponer sliders de
volumen y poco más.

### 16. Rama `ultima_version` en el remoto · impacto bajo · esfuerzo bajo

Quedó una rama vieja publicada en el fork. Se puede borrar una vez confirmado
que su contenido está en `main`.

### 17. Fuente tipográfica ausente · impacto bajo · esfuerzo bajo

El juego busca `src/assets/fonts/04B_11__.TTF` y, al no encontrarla, usa la
fuente por defecto de Pygame. Conviene **incluir la fuente** (si su licencia lo
permite) o **cambiar a una fuente libre** equivalente y documentarlo.

---

## Lo que ya está bien

No todo son mejoras pendientes. Vale la pena conservar:

- **Separación por capas** (`scenes` / `entities` / `service` / `db` /
  `constants`) clara y consistente.
- **Patrón de escena uniforme** (`handle_event` / `update` / `draw`).
- **Delta time** en todo el movimiento — el juego es estable a cualquier FPS.
- **Carga defensiva de recursos**: si falta un sprite o un sonido, el juego
  degrada en vez de crashear.
- **`Database`** encapsula bien el acceso a SQLite.
- **`AudioManager`** con música contextual y transiciones suaves.
