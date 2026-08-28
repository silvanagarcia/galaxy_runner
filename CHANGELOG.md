# Changelog

Todos los cambios relevantes de este proyecto se documentan en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## [Sin publicar]

### Reorganización estructural del repositorio

Cambios de estructura y documentación. **La lógica del juego no se modificó.**

#### Estructura

- Carpeta `Code/` renombrada a `src/`.
- `GalaxyRunner.spec`, `build.bat` y el icono movidos a `build/`.
- Capturas de pantalla movidas a `docs/screenshots/`.
- Documento de diseño movido a `docs/` (además, versión en Markdown).
- Eliminada la carpeta vacía `src/repository/`.
- Eliminada la copia duplicada de assets (`assets/**/_internal/`).

#### Higiene del repositorio

- **Reescritura del historial de Git** para purgar binarios pesados:
  `dist/` (build de Windows con DLLs), la base de datos `galaxy.db`,
  `error.log`, el acceso directo `.lnk` y los `__pycache__/`.
  El repositorio pasó de ~370 MB a un tamaño acorde al código y los assets.
- Nuevo `.gitignore` completo (Python, PyInstaller, `*.db`, logs, SO).
- La base de datos ya **no se versiona**: se genera sola al ejecutar el juego.

#### Documentación

- `README.md` reescrito: instalación, ejecución, controles, tablas de
  balance (niveles, power-ups, puntuación), esquema de base de datos,
  estructura real del proyecto y roadmap.
- Nuevos `LICENSE` (MIT), `docs/ARQUITECTURA.md` y `docs/CREDITOS.md`.

#### Ajustes mínimos de rutas (necesarios por el renombrado de carpeta)

- `src/service/background_animation.py`: `from Code.constants.config import …`
  → `from constants.config import …` (alinea el archivo con el resto de los
  módulos, que ya usaban imports relativos al paquete).
- `src/constants/config.py`: la ruta del *build* de PyInstaller pasa de
  `…/Code` a `…/src`.

### Pendiente

- Actualizar los scripts de `build/` (siguen apuntando a `Code/`).
- Implementar la pantalla de Opciones.
- Unificar `constants/config.py` con `UI/ui.py`.
