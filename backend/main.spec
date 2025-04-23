# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# SQLite veritabanı dosyasının yolu
db_path = os.path.join(os.path.dirname(os.path.abspath('__file__')), 'mydata.db')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # SQLite veritabanını dahil et
        (db_path, '.'),
    ],
    hiddenimports=[
        'flask',
        'flask_cors',
        'flask_jwt_extended',
        'flask_bcrypt',
        'sqlite3',
        'dotenv',
        'json',
        'config',
        'services',
        'models',
        'hill_climbing_algorithm',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Konsol penceresi gösterme
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
