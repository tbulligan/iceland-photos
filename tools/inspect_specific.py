import os
from PIL import Image

SOURCE = '/mnt/c/Users/tomas/Pictures/2026-Islanda'

# Let's inspect the files mentioned
inspect_files = [
    'PXL_20261028_154753043.jpg',
    'PXL_20261029_153953441.jpg',
    'PXL_20261029_162106798.jpg',
    'PXL_20261029_162555366.jpg',
    'PXL_20261029_163623608.jpg',
    'PXL_20261030_094030441.jpg',
    'PXL_20261030_102016214.jpg',
    'PXL_20261030_102316998.jpg',
    'PXL_20261030_103618991.jpg',
    'PXL_20261030_104911635.jpg',
    'PXL_20261030_113703709.jpg',
    'PXL_20261031_123137430.jpg',
    'PXL_20261031_123856453.jpg',
    'PXL_20261031_130343902.jpg',
    'PXL_20261031_130448667.jpg',
    'PXL_20261031_133314715.jpg',
    'PXL_20261031_140732367.jpg'
]

for f in inspect_files:
    p = os.path.join(SOURCE, f)
    if os.path.exists(p):
        im = Image.open(p)
        print(f"{f}: size={im.size}, mode={im.mode}")
    else:
        print(f"NOT FOUND: {f}")
