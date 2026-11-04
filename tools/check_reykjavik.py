import os
from PIL import Image

SOURCE_DIR = '/mnt/c/Users/tomas/Pictures/2026-Islanda'
r_files = [
    'PXL_20261022_095104303.jpg',
    'PXL_20261022_101624879~2.jpg',
    'PXL_20261022_113959206.jpg',
    'PXL_20261024_163848333.jpg',
    'PXL_20261024_231405953.NIGHT.jpg',
    'PXL_20261025_153150352.jpg',
    'PXL_20261025_154614300.jpg',
    'PXL_20261025_155439449.jpg',
    'PXL_20261025_182708204.jpg',
    'PXL_20261025_183531541.jpg',
    'PXL_20261025_185719775.jpg',
    'PXL_20261026_161203144.jpg',
    'PXL_20261026_162737009.jpg',
    'PXL_20261026_163647963.jpg',
    'PXL_20261026_172852238.jpg',
    'PXL_20261026_173005914.jpg',
    'PXL_20261026_173143349.jpg',
    'PXL_20261028_122746447.jpg',
    'PXL_20261028_162347353.jpg',
    'PXL_20261028_175708712.jpg',
    'PXL_20261028_181128651.jpg',
    'PXL_20261028_185328787.jpg',
    'PXL_20261031_211327423.jpg'
]

for f in r_files:
    fp = os.path.join(SOURCE_DIR, f)
    if os.path.exists(fp):
        im = Image.open(fp)
        print(f"{f}: size={im.size}")
