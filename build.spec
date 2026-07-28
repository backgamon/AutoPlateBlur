# -*- mode: python -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
    ('ffmpeg.exe','.')
],
    ],
    hiddenimports=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AutoPlateBlur_V1',
    debug=False,
    strip=False,
    upx=True,
    console=False,
)
