# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['desktop.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('static', 'static'),
        ('requirements.txt', '.'),
        ('uploads', 'uploads'),
    ],
    hiddenimports=[
        'uvicorn.logging',
        'uvicorn.protocols',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
        'uvicorn.lifespan.off',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'fastapi',
        'starlette',
        'pydantic',
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DoiChieuExcel',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'  
)
