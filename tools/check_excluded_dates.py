import os, json
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif(path):
    try:
        img = Image.open(path)
        exif = img._getexif()
        if not exif: return {}
        data = {}
        for tag, val in exif.items():
            name = TAGS.get(tag, tag)
            data[name] = val
        return data
    except Exception:
        return {}

src_dir = '/mnt/c/Users/tomas/Pictures/2026-Islanda'
with open('data.json') as f:
    curr = {p['filename'] for p in json.load(f)}

excluded = [f for f in sorted(os.listdir(src_dir)) if f.lower().endswith(('.jpg', '.jpeg')) and f not in curr]

print(f'Checking {len(excluded)} excluded photos...')
for f in excluded:
    path = os.path.join(src_dir, f)
    ex = get_exif(path)
    dt = ex.get('DateTimeOriginal', ex.get('DateTime', 'Unknown'))
    print(f'{f} | {dt}')
