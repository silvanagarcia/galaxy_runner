# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

# Configurar el path base
code_path = os.path.join(os.getcwd(), 'Code')

a = Analysis(
    ['Code\\main.py'],
    pathex=[code_path],  # Agregar Code al path para que encuentre los módulos
    binaries=[],
    datas=[
        ('Code\\assets\\images', 'assets\\images'),
        ('Code\\assets\\sounds', 'assets\\sounds'),
        ('Code\\assets\\backgrounds', 'assets\\backgrounds'),
        ('Code\\assets\\fonts', 'assets\\fonts'),
        ('Code\\db\\galaxy.db', 'db'),  # Incluir la base de datos
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
