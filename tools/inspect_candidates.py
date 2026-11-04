import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

src_dir = '/mnt/c/Users/tomas/Pictures/2026-Islanda'
files = [
    'PXL_20261021_081252444.jpg',
    'PXL_20261024_163848333.jpg',
    'PXL_20261025_153150352.jpg',
    'PXL_20261025_154614300.jpg',
    'PXL_20261026_161203144.jpg',
    'PXL_20261028_122746447.jpg',
    'PXL_20261030_113703709.jpg',
    'PXL_20261031_130448667.jpg',
    'PXL_20261031_133314715.jpg',
    'PXL_20261031_141754942.jpg'
]

def to_deg(val):
    d = float(val[0])
    m = float(val[1])
    s = float(val[2])
    return d + (m / 60.0) + (s / 3600.0)

for f in files:
    p = os.path.join(src_dir, f)
    if not os.path.exists(p): continue
    img = Image.open(p)
    ex = img._getexif() or {}
    dt = ex.get(36867, ex.get(306, ''))
    gps = ex.get(34853, {})
    lat = lon = None
    if 2 in gps and 4 in gps:
        lat = to_deg(gps[2]) * (-1 if gps.get(1) == 'S' else 1)
        lon = to_deg(gps[4]) * (-1 if gps.get(3) == 'W' else 1)
    print(f'{f} | {dt} | coords: ({lat}, {lon}) | size: {img.size}')
