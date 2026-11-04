import os, sys
from PIL import Image, ExifTags

SOURCE = '/mnt/c/Users/tomas/Pictures/2026-Islanda'

def get_exif(path):
    try:
        im = Image.open(path)
        exif = im._getexif()
        if not exif: return {}
        res = {}
        for k, v in exif.items():
            name = ExifTags.TAGS.get(k, k)
            res[name] = v
        return res
    except Exception:
        return {}

def dms_to_deg(dms, ref):
    if not dms: return None
    try:
        deg = float(dms[0])
        minute = float(dms[1])
        sec = float(dms[2])
        dec = deg + minute / 60.0 + sec / 3600.0
        if ref in ['S', 'W']: dec = -dec
        return round(dec, 5)
    except Exception:
        return None

def parse_gps(exif):
    gps_info = exif.get('GPSInfo')
    if not gps_info: return None
    gps = {}
    for k, v in gps_info.items():
        name = ExifTags.GPSTAGS.get(k, k)
        gps[name] = v
    lat = dms_to_deg(gps.get('GPSLatitude'), gps.get('GPSLatitudeRef'))
    lon = dms_to_deg(gps.get('GPSLongitude'), gps.get('GPSLongitudeRef'))
    if lat and lon:
        return (lat, lon)
    return None

all_files = []
for root, dirs, files in os.walk(SOURCE):
    for f in files:
        if f.lower().endswith(('.jpg', '.jpeg')):
            full_path = os.path.join(root, f)
            rel_dir = os.path.relpath(root, SOURCE)
            ex = get_exif(full_path)
            dt = ex.get('DateTimeOriginal') or ex.get('DateTime') or ''
            coords = parse_gps(ex)
            all_files.append((dt, f, rel_dir, coords, full_path))

all_files.sort(key=lambda x: (x[0], x[1]))

print(f"Total photos found: {len(all_files)}")
for dt, f, rel_dir, coords, full_path in all_files:
    folder = f"[{rel_dir}] " if rel_dir != '.' else ""
    coord_str = f"({coords[0]}, {coords[1]})" if coords else "no GPS"
    print(f"{dt} | {folder}{f} | {coord_str}")
