import os
import sys
import json
import shutil
from PIL import Image, ImageOps, ExifTags

BASE_DIR = '/home/tomaso/projects/iceland-photos'
SOURCE_DIR = '/mnt/c/Users/tomas/Pictures/2026-Islanda'
PHOTOS_DIR = os.path.join(BASE_DIR, 'photos')
THUMBS_DIR = os.path.join(BASE_DIR, 'thumbs')
DATA_FILE = os.path.join(BASE_DIR, 'data.json')

# Anchor coordinates for dive sites
COORDS_SILFRA = (64.25643, -21.11661)
COORDS_DAVID = (64.23617, -21.04493)

NEW_PHOTOS = [
    # Westfjords & Aurora
    ('PXL_20261020_152435767~2.jpg', 'Strandir Peninsula Arctic Sea Cliffs', 'Strandir Coast • Westfjords'),
    ('PXL_20261020_223127604.NIGHT.jpg', 'First Aurora Glow', 'Drangsnes Sky • Westfjords'),

    # Golden Circle
    ('PXL_20261021_151106273.jpg', 'Strokkur Boiling Vent & Steam Plume', 'Geysir Geothermal Area'),
    ('PXL_20261021_161826637~2.jpg', 'Gullfoss Canyon Upper Tier', 'Gullfoss Canyon'),

    # Reykjavík
    ('PXL_20261024_163848333.jpg', 'Reykjavík Old Harbor & Mt. Esja', 'Reykjavík Waterfront'),
    ('PXL_20261024_231405953.NIGHT.jpg', 'Harbor Aurora Reflection', 'Grótta • Reykjavík'),
    ('PXL_20261025_154614300.jpg', 'Historic Corrugated Iron Architecture', 'Reykjavík Downtown'),
    ('PXL_20261026_161203144.jpg', 'Sun Voyager (Sólfar) Sculpture', 'Reykjavík Waterfront'),
    ('PXL_20261026_162737009.jpg', 'Faxaflói Bay Promenade', 'Reykjavík Coast'),

    # Scuba
    ('PXL_20261027_130347123.jpg', 'Silfra Dive Preparation & Staging Platform', 'Silfra • Þingvellir'),
    ('IMG_4711.JPG', 'Davíðsgjá Ascent & Sunburst', 'Davíðsgjá • Lake Þingvallavatn (Dive 2)'),
    ('PXL_20261027_133843596.jpg', 'Lake Þingvallavatn Dive Exit Shoreline', 'Davíðsgjá • Lake Þingvallavatn'),

    # Museum & City
    ('PXL_20261028_122746447.jpg', 'Tjörnin Lake Autumn Promenade', 'Tjörnin • Reykjavík'),
    ('PXL_20261028_142124937.jpg', 'Viking Age Silver Hoards & Relics', 'National Museum of Iceland (Þjóðminjasafn)'),
    ('PXL_20261028_143748446.jpg', 'Valþjófsstaður Medieval Carved Door', 'National Museum of Iceland (Þjóðminjasafn)'),

    # Glacier Lagoons & Diamond Beach
    ('PXL_20261029_140136936.jpg', 'Black Sand Ice Sculpture', 'Diamond Beach • Breiðamerkursandur'),
    ('PXL_20261029_144151472.jpg', 'Sculpted Blue Iceberg Arches', 'Jökulsárlón Glacier Lagoon'),
    ('PXL_20261029_162106798.jpg', 'Fjallsárlón Glacier Tongue & Terminal Lake', 'Fjallsárlón Glacier Lagoon'),
    ('PXL_20261029_163826694.jpg', 'Calving Glacier Wall Detail', 'Fjallsárlón Glacier Lagoon'),

    # Falljökull Ice Cave
    ('PXL_20261030_093228132.jpg', 'Falljökull Proglacial Outwash Plain', 'Falljökull • Vatnajökull National Park'),
    ('PXL_20261030_102338388.jpg', 'Ascending Falljökull Lateral Moraine', 'Falljökull • Vatnajökull National Park'),
    ('PXL_20261030_111446663.jpg', 'Glacial Moulin & Sapphire Shaft', 'Falljökull Ice Cave • Vatnajökull'),
    ('PXL_20261030_113703709.jpg', 'Falljökull Icefall Panoramic Overlook', 'Falljökull • Vatnajökull National Park'),

    # South Coast
    ('PXL_20261030_144641655.jpg', 'Eldhraun Vast Moss Lava Field', 'Eldhraun Lava Field'),
    ('PXL_20261030_155507298.jpg', 'Reynisdrangar Sea Stacks from Vík', 'Vík í Mýrdal'),
    ('PXL_20261030_163530113.jpg', 'Hálsanefshellir Basalt Columns', 'Reynisfjara Beach'),
    ('PXL_20261030_174357592.jpg', 'Skógá River Canyon Cascades', 'Skógá River • South Coast'),
    ('PXL_20261030_182322356.NIGHT.jpg', 'Cavern Passage Behind Seljalandsfoss', 'Seljalandsfoss Waterfall'),

    # Snæfellsnes
    ('PXL_20261031_105933217.jpg', 'Kirkjufell Autumn Reflections', 'Grundarfjörður • Snæfellsnes'),
    ('PXL_20261031_123419469.jpg', 'Djúpalónssandur Black Pebble Cove', 'Djúpalónssandur • Snæfellsnes'),
    ('PXL_20261031_130448667.jpg', 'Epine Trawler Rusted Hull Fragments', 'Djúpalónssandur • Snæfellsnes'),
    ('PXL_20261031_133833097.jpg', 'Svalþúfa Sea Cliff Trail', 'Lóndrangar • Snæfellsnes'),
    ('PXL_20261031_140115572.jpg', 'Arnarstapi Roaring Sea Blowhole', 'Arnarstapi Coast'),
    ('PXL_20261031_153459957.jpg', 'Búðahraun Ancient Lava Field', 'Búðir • Snæfellsnes')
]

def to_deg(dms):
    return float(dms[0]) + float(dms[1]) / 60.0 + float(dms[2]) / 3600.0

def format_date_display(dt_str):
    if not dt_str or len(dt_str) < 10: return ''
    parts = dt_str.split(' ')
    ymd = parts[0].split(':')
    if len(ymd) != 3: return dt_str
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    try:
        m = month_names[int(ymd[1]) - 1]
        time_part = parts[1][:5] if len(parts) > 1 else ''
        return f"{m} {int(ymd[2])} • {time_part}" if time_part else f"{m} {int(ymd[2])}"
    except Exception:
        return dt_str

def find_file(fname):
    for root, dirs, files in os.walk(SOURCE_DIR):
        if fname in files:
            return os.path.join(root, fname)
    return None

def main():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        existing_photos = json.load(f)

    existing_filenames = {p['filename'] for p in existing_photos}
    print(f"Current photo count: {len(existing_photos)}")

    new_entries = []
    for fname, title, place in NEW_PHOTOS:
        if fname in existing_filenames:
            print(f"Skipping {fname} (already present)")
            continue

        src_path = find_file(fname)
        if not src_path:
            raise FileNotFoundError(f"Could not locate source file: {fname}")

        dst_photo = os.path.join(PHOTOS_DIR, fname)
        dst_thumb = os.path.join(THUMBS_DIR, fname)

        # 1. Copy photo
        shutil.copy2(src_path, dst_photo)

        # 2. Extract EXIF and create thumbnail
        with Image.open(src_path) as img:
            transposed = ImageOps.exif_transpose(img)
            w, h = transposed.size
            aspect = round(w / h, 3)

            # Thumbnail
            thumb = transposed.copy()
            thumb.thumbnail((720, 720), Image.Resampling.LANCZOS)
            if thumb.mode in ('RGBA', 'P'):
                thumb = thumb.convert('RGB')
            thumb.save(dst_thumb, 'JPEG', quality=84, optimize=True)

            exif = img.getexif()
            exif_ifd = exif.get_ifd(0x8769) if exif else None
            dt_str = (exif_ifd.get(36867) or exif_ifd.get(36868) or exif.get(306)) if exif_ifd else (exif.get(306) if exif else '')

            # Dive camera 2023 clock fix
            if fname.startswith('IMG_') and dt_str and dt_str.startswith('2023:11:03'):
                dt_str = dt_str.replace('2023:11:03', '2026:10:27')

            gps_info = exif.get_ifd(ExifTags.IFD.GPSInfo) if exif else None
            lat = lon = None
            if gps_info and 2 in gps_info and 4 in gps_info:
                try:
                    raw_lat = to_deg(gps_info[2])
                    if gps_info.get(1) == 'S': raw_lat = -raw_lat
                    raw_lon = to_deg(gps_info[4])
                    if gps_info.get(3) == 'W': raw_lon = -raw_lon
                    lat = round(raw_lat, 6)
                    lon = round(raw_lon, 6)
                except Exception:
                    pass

            if lat is None:
                if 'Silfra' in place:
                    lat, lon = COORDS_SILFRA
                elif 'Davíðsgjá' in place or 'David' in place:
                    lat, lon = COORDS_DAVID

        entry = {
            'filename': fname,
            'title': title,
            'place': place,
            'is_hero': False,
            'datetime': dt_str or '',
            'date_display': format_date_display(dt_str),
            'lat': lat,
            'lon': lon,
            'thumb': f"thumbs/{fname}",
            'src': f"photos/{fname}",
            'aspect': aspect
        }
        new_entries.append(entry)
        print(f"Added [{fname}] -> {title} ({place}) | {dt_str} | coords: ({lat}, {lon})")

    # Combine existing + new
    all_photos = existing_photos + new_entries

    # Chronological sort
    for p in all_photos:
        dt = p.get('datetime', '')
        if dt.startswith('2023:11:03'):
            p['sort_key'] = dt.replace('2023:11:03', '2026:10:27')
        else:
            p['sort_key'] = dt

    all_photos.sort(key=lambda x: (x['sort_key'], x['filename']))
    for p in all_photos:
        del p['sort_key']

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_photos, f, indent=2, ensure_ascii=False)

    print(f"\nFinal photo count in data.json: {len(all_photos)}")

if __name__ == '__main__':
    main()
