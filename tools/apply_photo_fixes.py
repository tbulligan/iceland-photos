import os, json, shutil
from PIL import Image, ImageOps

BASE_DIR = '/home/tomaso/projects/iceland-photos'
SRC_DIR = '/mnt/c/Users/tomas/Pictures/2026-Islanda'
DATA_FILE = os.path.join(BASE_DIR, 'data.json')
PHOTOS_DIR = os.path.join(BASE_DIR, 'photos')
THUMBS_DIR = os.path.join(BASE_DIR, 'thumbs')

# 1. Prepare new real Aurora photo
new_aurora_fname = 'PXL_20261022_215442711.NIGHT.jpg'
src_path = os.path.join(SRC_DIR, new_aurora_fname)
dst_photo = os.path.join(PHOTOS_DIR, new_aurora_fname)
dst_thumb = os.path.join(THUMBS_DIR, new_aurora_fname)

shutil.copy2(src_path, dst_photo)

# Create optimized thumb
img = Image.open(src_path)
img = ImageOps.exif_transpose(img)
img.thumbnail((720, 540), Image.Resampling.LANCZOS)
img.save(dst_thumb, 'JPEG', quality=82, optimize=True)

# Remove old cloudy photo
old_cloudy = 'PXL_20261024_231405953.NIGHT.jpg'
for d in [PHOTOS_DIR, THUMBS_DIR]:
    p = os.path.join(d, old_cloudy)
    if os.path.exists(p):
        os.remove(p)

# 2. Update data.json
with open(DATA_FILE) as f:
    data = json.load(f)

new_data = []
for p in data:
    fn = p['filename']
    if fn == old_cloudy:
        # Replace with real aurora
        new_entry = {
            'filename': new_aurora_fname,
            'title': 'Reykjavík Aurora Borealis Vortex',
            'place': 'Reykjavík Night Sky',
            'lat': 64.14484,
            'lon': -21.88945,
            'date': '2026:10:22 21:54:42',
            'date_display': 'Oct 22 • 21:54',
            'is_hero': True,
            'src': f'photos/{new_aurora_fname}',
            'thumb': f'thumbs/{new_aurora_fname}'
        }
        new_data.append(new_entry)
        continue

    if fn == 'PXL_20261022_101624879~2.jpg':
        p['title'] = 'Hallgrímskirkja Grand Pipe Organ'
        p['place'] = 'Hallgrímskirkja • Reykjavík'
    elif fn == 'PXL_20261022_113959206.jpg':
        p['title'] = 'Harpa Concert Hall Geometric Interior'
        p['place'] = 'Harpa • Reykjavík Harbor'
    elif fn == 'PXL_20261026_163647963.jpg':
        p['title'] = 'Cooling Molten Lava Flow'
        p['place'] = 'Icelandic Lava Show • Reykjavík'
    elif fn == 'PXL_20261020_082333462.jpg':
        p['title'] = 'Icelandic Verse on Fjord Bench'
        p['place'] = 'Drangsnes • Strandir'
    elif fn == 'PXL_20261020_152145792.jpg':
        p['title'] = 'Hólmavíkurkirkja over Steingrímsfjörður'
        p['place'] = 'Hólmavík • Westfjords'

    new_data.append(p)

# Sort strictly chronologically by date
new_data.sort(key=lambda x: x.get('date', ''))

with open(DATA_FILE, 'w') as f:
    json.dump(new_data, f, indent=2)

print(f'Successfully updated data.json with {len(new_data)} photos.')
