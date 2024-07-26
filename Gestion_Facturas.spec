# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(
    ['session.py'],
    pathex=['C:/xampp/htdocs/MIS_PROYECTOS/SISTEMA_FACTURACION','C:/xampp/htdocs/MIS_PROYECTOS/SISTEMA_FACTURACION/controllers', 'C:/xampp/htdocs/MIS_PROYECTOS/SISTEMA_FACTURACION/views', 'C:/xampp/htdocs/MIS_PROYECTOS/SISTEMA_FACTURACION/utils', 'C:/xampp/htdocs/MIS_PROYECTOS/SISTEMA_FACTURACION/img'],
    binaries=[],
    datas=[('C:/xampp/htdocs/MIS_PROYECTOS/SISTEMA_FACTURACION/img', 'img')],
    hiddenimports=['babel.numbers'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Gestion_Facturas',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['logo_app.ico'],
)
