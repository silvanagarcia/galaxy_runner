# -*- mode: python ; coding: utf-8 -*-
#
# TODO (post-reorganización): este spec fue migrado de `Code/` a `src/`.
# Pendiente de revisión completa:
#   - ejecutar siempre desde la raíz del repo:  pyinstaller build/GalaxyRunner.spec
#   - `src/assets/backgrounds` y `src/assets/fonts` no existen todavía (assets opcionales)
#   - la base de datos ya no se versiona; se genera al primer arranque
#
import os

block_cipher = None

# Configurar el path base (raíz del repo / carpeta src)
code_path = os.path.join(os.getcwd(), 'src')

a = Analysis(
    [os.path.join('src', 'main.py')],
    pathex=[code_path],  # Agregar src al path para que encuentre los módulos
    binaries=[],
    datas=[
        (os.path.join('src', 'assets', 'images'), os.path.join('assets', 'images')),
        (os.path.join('src', 'assets', 'sounds'), os.path.join('assets', 'sounds')),
    ],
    hiddenimports=[
        'db',
        'db.db_manager',
        'constants',
        'constants.config',
        'UI',
        'UI.ui',
        'UI.intro_screen',
        'scenes',
        'scenes.start_menu',
        'scenes.game_scene',
        'scenes.leaderboard_scene',
        'scenes.game_over_scene',
        'scenes.options_scene',
        'scenes.credits_scene',
        'service',
        'service.audio_manager',
        'service.background_animation',
        'entities',
        'entities.player',
        'entities.enemigos',
        'entities.boss',
        'entities.meteorito',
        'entities.proyectiles',
        'entities.powerup',
        'entities.explosiones',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='GALAXY-RUNNER',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Sin consola
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GALAXY-RUNNER',
)
