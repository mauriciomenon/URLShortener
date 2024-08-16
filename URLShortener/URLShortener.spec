# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['URLshortener.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['pyshorteners', 'pyshorteners.shorteners', 'pyshorteners.shorteners.tinyurl'],
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
    console=False,  # Certifique-se de que esta linha esteja presente e definida como False
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='default.icns',  # Remova ou comente esta linha para evitar problemas com o ícone
)

app = BUNDLE(
    exe,
    name='URLShortener.app',
    # icon='default.icns',  # Remova ou comente esta linha para evitar problemas com o ícone
    bundle_identifier=None,
)
