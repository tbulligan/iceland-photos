import os
import json
import shutil
from PIL import Image, ImageOps, ExifTags

BASE_DIR = '/home/tomaso/projects/iceland-photos'
SRC_DIR = '/mnt/c/Users/tomas/Pictures/2026-Islanda'
DATA_FILE = os.path.join(BASE_DIR, 'data.json')
PHOTOS_DIR = os.path.join(BASE_DIR, 'photos')
THUMBS_DIR = os.path.join(BASE_DIR, 'thumbs')

# 1. Photos to prune
PRUNE_FILES = [
    'PXL_20261020_082333462.jpg',          # Bench with verse & cars
    'PXL_20261020_223127604.NIGHT.jpg',    # Weak aurora glow
    'PXL_20261020_230829906.NIGHT.jpg',    # Double aurora arch (redundant)
]

# 2. Photos to add with curated metadata
ADD_PHOTOS = [
    {
        'filename': 'PXL_20261021_081252444.jpg',
        'title': 'Strandir Valley Autumn Frost',
        'place': 'Drangsnes • Westfjords',
        'fallback_lat': 65.7811,
        'fallback_lon': -21.5191,
        'datetime': '2026:10:21 08:12:52',
        'date_display': 'Oct 21 • 08:12',
        'is_hero': True
    },
    {
        'filename': 'PXL_20261029_162720896.jpg',
        'title': 'Crystal Cave Tephra Layers & Fluted Ice',
        'place': 'Vatnajökull Ice Cave',
        'fallback_lat': 64.0489,
        'fallback_lon': -16.1806,
        'datetime': '2026:10:29 16:27:20',
        'date_display': 'Oct 29 • 16:27',
        'is_hero': True
    },
    {
        'filename': 'PXL_20261030_102417128.jpg',
        'title': 'Falljökull Glacier Crevasse Field',
        'place': 'Falljökull • Vatnajökull',
        'fallback_lat': 63.9734,
        'fallback_lon': -16.8003,
        'datetime': '2026:10:30 10:24:17',
        'date_display': 'Oct 30 • 10:24',
        'is_hero': True
    },
    {
        'filename': 'PXL_20261031_133314715.jpg',
        'title': 'Lóndrangar Ocean Promontory & Rain Squall',
        'place': 'Lóndrangar • Snæfellsnes',
        'fallback_lat': 64.7352,
        'fallback_lon': -23.7742,
        'datetime': '2026:10:31 13:33:14',
        'date_display': 'Oct 31 • 13:33',
        'is_hero': True
    },
    {
        'filename': 'PXL_20261031_141754942.jpg',
        'title': 'Arnarstapi Basalt Sea Cliffs',
        'place': 'Arnarstapi • Snæfellsnes',
        'fallback_lat': 64.7678,
        'fallback_lon': -23.6170,
        'datetime': '2026:10:31 14:17:54',
        'date_display': 'Oct 31 • 14:17',
        'is_hero': True
    }
]

def get_gps_and_aspect(filepath, fallback_lat, fallback_lon):
    with Image.open(filepath) as img:
        transposed = ImageOps.exif_transpose(img)
        w, h = transposed.size
        aspect = round(w / h, 3)

        lat = fallback_lat
        lon = fallback_lon

        exif = img.getexif()
        if exif:
            gps_info = exif.get_ifd(ExifTags.IFD.GPSInfo)
            if gps_info:
                def to_deg(dms):
                    return float(dms[0]) + float(dms[1])/60.0 + float(dms[2])/3600.0
                try:
                    raw_lat = to_deg(gps_info[2])
                    if gps_info.get(1) == 'S': raw_lat = -raw_lat
                    raw_lon = to_deg(gps_info[4])
                    if gps_info.get(3) == 'W': raw_lon = -raw_lon
                    lat = round(raw_lat, 6)
                    lon = round(raw_lon, 6)
                except Exception as e:
                    pass

    return lat, lon, aspect

def main():
    # 1. Prune files from disk
    for fn in PRUNE_FILES:
        p_photo = os.path.join(PHOTOS_DIR, fn)
        p_thumb = os.path.join(THUMBS_DIR, fn)
        if os.path.exists(p_photo):
            os.remove(p_photo)
            print(f"Removed photo: {fn}")
        if os.path.exists(p_thumb):
            os.remove(p_thumb)
            print(f"Removed thumb: {fn}")

    # 2. Add new photos to photos/ and thumbs/
    new_entries = []
    for item in ADD_PHOTOS:
        fn = item['filename']
        src_path = os.path.join(SRC_DIR, fn)
        dst_photo = os.path.join(PHOTOS_DIR, fn)
        dst_thumb = os.path.join(THUMBS_DIR, fn)

        if not os.path.exists(src_path):
            raise FileNotFoundError(f"Source file not found: {src_path}")

        # Copy original
        shutil.copy2(src_path, dst_photo)

        # Generate thumbnail
        with Image.open(src_path) as img:
            transposed = ImageOps.exif_transpose(img)
            transposed.thumbnail((720, 540), Image.Resampling.LANCZOS)
            transposed.save(dst_thumb, 'JPEG', quality=82, optimize=True)

        lat, lon, aspect = get_gps_and_aspect(src_path, item['fallback_lat'], item['fallback_lon'])

        entry = {
            'filename': fn,
            'title': item['title'],
            'place': item['place'],
            'is_hero': item['is_hero'],
            'datetime': item['datetime'],
            'date_display': item['date_display'],
            'lat': lat,
            'lon': lon,
            'thumb': f'thumbs/{fn}',
            'src': f'photos/{fn}',
            'aspect': aspect
        }
        new_entries.append(entry)
        print(f"Processed new photo: {fn} (aspect: {aspect}, lat: {lat}, lon: {lon})")

    # 3. Update data.json
    with open(DATA_FILE) as f:
        data = json.load(f)

    # Filter out pruned files
    filtered = []
    for p in data:
        if p['filename'] in PRUNE_FILES:
            continue
        # Ensure consistent datetime field
        if 'datetime' not in p and 'date' in p:
            p['datetime'] = p['date']
        filtered.append(p)

    # Add new entries
    filtered.extend(new_entries)

    # Sort strictly chronologically by datetime
    filtered.sort(key=lambda x: x.get('datetime', ''))

    with open(DATA_FILE, 'w') as f:
        json.dump(filtered, f, indent=2)

    print(f"\nFinal count in data.json: {len(filtered)} photos (Expected: 60)")
    assert len(filtered) == 60, f"Expected 60 photos, got {len(filtered)}"

if __name__ == '__main__':
    main()
