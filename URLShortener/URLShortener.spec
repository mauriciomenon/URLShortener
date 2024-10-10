# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['URLshortener.py'],  # Substitua pelo nome real do seu arquivo principal
    pathex=[],
    binaries=[],
    datas=[
        ('C:\\msys64\\ucrt64\\lib\\python3.11\\site-packages\\pyshorteners', 'pyshorteners'),
        ('C:\\msys64\\ucrt64\\lib\\python3.11\\site-packages\\PIL', 'PIL'),
        ('C:\\msys64\\ucrt64\\lib\\python3.11\\site-packages\\qrcode', 'qrcode'),
        ('7208695_application_browser_internet_web_network_icon.ico', '.'),  # Inclui o ícone
    ],
    hiddenimports=[
        'pyshorteners',
        'pyshorteners.shorteners',
        'pyshorteners.shorteners.tinyurl',
        'pyshorteners.exceptions',
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
        'PIL.ImageFont',
        'qrcode',
        'PyQt6',
        'PyQt6.QtWidgets',
        'PyQt6.QtGui',
        'PyQt6.QtCore',
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
    name='URLShortener',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Defina como False se não quiser a janela do console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='7208695_application_browser_internet_web_network_icon.ico',  # Define o ícone do executável
)
