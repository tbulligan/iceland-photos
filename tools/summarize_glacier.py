import os
from PIL import Image

SOURCE_DIR = '/mnt/c/Users/tomas/Pictures/2026-Islanda'

def summarize_image(fname):
    fp = os.path.join(SOURCE_DIR, fname)
    if not os.path.exists(fp):
        fp = os.path.join(SOURCE_DIR, 'scuba-selected', fname)
    if not os.path.exists(fp):
        return f"{fname}: NOT FOUND"
    try:
        im = Image.open(fp)
        w, h = im.size
        # sample some colors or basic info
        return f"{fname}: size={w}x{h}"
    except Exception as e:
        return f"{fname}: err {e}"

files = [
    'PXL_20261029_153953441.jpg',
    'PXL_20261029_162106798.jpg',
    'PXL_20261029_162555366.jpg',
    'PXL_20261029_162720896.jpg',
    'PXL_20261029_163401862.jpg',
    'PXL_20261029_163623608.jpg',
    'PXL_20261029_163826694.jpg',
    'PXL_20261029_163851515.jpg',
    'PXL_20261030_093228132.jpg',
    'PXL_20261030_094030441.jpg',
    'PXL_20261030_102016214.jpg',
    'PXL_20261030_102316998.jpg',
    'PXL_20261030_103618991.jpg',
    'PXL_20261030_104201790.jpg',
    'PXL_20261030_104610152.jpg',
    'PXL_20261030_104911635.jpg',
    'PXL_20261030_111446663.jpg',
    'PXL_20261030_113703709.jpg',
    'PXL_20261030_115114450.jpg',
    'PXL_20261030_115513215.jpg',
]

for f in files:
    print(summarize_image(f))
