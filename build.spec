# -*- mode: python -*-

a = Analysis(
    ['main.py'],
    datas=[
        ('ffmpeg','ffmpeg')
    ],
    hiddenimports=[],
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    name='AutoPlateBlur_V1',
    console=False
)
