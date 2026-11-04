import os, sys, json, hashlib, shutil
from PIL import Image, ImageOps

SOURCE_DIR = '/mnt/c/Users/tomas/Pictures/2026-Islanda'
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
THUMBS_DIR = os.path.join(OUTPUT_DIR, 'thumbs')
PHOTOS_DIR = os.path.join(OUTPUT_DIR, 'photos')

# Anchor coordinates for dive sites
COORDS_SILFRA = (64.25643, -21.11661)
COORDS_DAVID = (64.23617, -21.04493)

# 22 HIGHLIGHT HEROES (Every key milestone, zero redundancy)
HERO_SELECTION = {
    # Westfjords & Northern Lights
    'PXL_20261020_230151948.NIGHT.jpg': ('Northern Lights Curtain', 'Drangsnes • Westfjords'),
    'PXL_20261020_230341065.NIGHT.jpg': ('Emerald Aurora Swirl', 'Drangsnes • Westfjords'),
    'PXL_20261020_230907609.NIGHT.jpg': ('Corona Explosion', 'Drangsnes • Westfjords'),
    # Golden Circle
    'PXL_20261021_150901402.jpg': ('Strokkur Eruption', 'Geysir Geothermal Area'),
    'PXL_20261021_161448972.jpg': ('Gullfoss Golden Waterfall', 'Gullfoss Canyon'),
    # Scuba Dives (Calibrated to 3 peak milestones)
    'IMG_4582.JPG': ('Between Two Continents', 'Silfra Fissure (Dive 1)'),
    'IMG_4616.JPG': ('Silfra Cathedral', 'Silfra Fissure (Dive 1)'),
    'IMG_4686.JPG': ('Davíðsgjá Deep Chasm', 'Davíðsgjá • Lake Þingvallavatn (Dive 2)'),
    # Glacier Lagoons & Diamond Beach
    'PXL_20261029_135850683.jpg': ('Diamond on Volcanic Black Sand', 'Diamond Beach'),
    'PXL_20261029_144743380.jpg': ('Floating Icebergs of Jökulsárlón', 'Jökulsárlón Glacier Lagoon'),
    'PXL_20261029_163623608.jpg': ('Glacier Lagoon Calving Ice Wall', 'Fjallsárlón Glacier Lagoon'),
    # Falljökull Ice Cave (Vatnajökull)
    'PXL_20261030_104201790.jpg': ('Glacial Eye Arch Portal', 'Falljökull Ice Cave • Vatnajökull'),
    'PXL_20261030_104911635.jpg': ('Sapphire Ice Chamber', 'Falljökull Ice Cave • Vatnajökull'),
    # South Coast
    'PXL_20261030_144833807.jpg': ('Eldhraun Moss Lava Fields', 'Eldhraun Lava Field'),
    'PXL_20261030_163330009.jpg': ('Reynisfjara Black Sand Beach', 'Reynisfjara Beach'),
    'PXL_20261030_173120852.jpg': ('Skógafoss Waterfall', 'Skógar • South Coast'),
    'PXL_20261030_183431300.NIGHT.jpg': ('Seljalandsfoss Night Illumination', 'Seljalandsfoss Waterfall'),
    # Snæfellsnes Peninsula
    'PXL_20261031_110103448.jpg': ('Kirkjufell Mountain', 'Grundarfjörður • Snæfellsnes'),
    'PXL_20261031_123856453.jpg': ('Djúpalónssandur Beach & Epine Trawler Wreck', 'Djúpalónssandur • Snæfellsnes'),
    'PXL_20261031_132850938.jpg': ('Lóndrangar Basalt Pinnacles', 'Lóndrangar • Snæfellsnes'),
    'PXL_20261031_140732367.jpg': ('Gatklettur Natural Sea Arch', 'Arnarstapi Coast'),
    'PXL_20261031_150329519.jpg': ('Búðakirkja Black Church', 'Búðir • Snæfellsnes'),
}

# CURATED PRUNED JOURNEY (Non-redundant, pure travel signal)
JOURNEY_ALLOWED = {
    # Westfjords
    'PXL_20261018_085524369.jpg': ('Drangsnes Morning Ocean', 'Drangsnes • Westfjords'),
    'PXL_20261018_113935025.jpg': ('Steingrímsfjörður Coast', 'Westfjords Coastal Route'),
    'PXL_20261019_153620980.jpg': ('Hólmavík Fjord', 'Hólmavík • Westfjords'),
    'PXL_20261020_082333462.jpg': ('Strandir Morning Frost', 'Drangsnes Coast'),
    'PXL_20261020_152145792.jpg': ('Arctic Coastal Cliffs', 'Strandir Peninsula'),
    'PXL_20261021_091653823.jpg': ('Mountain Pass Descent', 'Westfjords Mountain Route'),

    # Aurora Progression
    'PXL_20261020_223127604.NIGHT.jpg': ('First Aurora Glow', 'Drangsnes Sky'),
    'PXL_20261020_230151948.NIGHT.jpg': ('Northern Lights Curtain', 'Drangsnes • Westfjords'),
    'PXL_20261020_230341065.NIGHT.jpg': ('Emerald Aurora Swirl', 'Drangsnes • Westfjords'),
    'PXL_20261020_230644730.NIGHT.jpg': ('Aurora Over the Fjord', 'Strandir Coast'),
    'PXL_20261020_230829906.NIGHT.jpg': ('Double Aurora Arch', 'Drangsnes Sky'),
    'PXL_20261020_230907609.NIGHT.jpg': ('Corona Explosion', 'Drangsnes • Westfjords'),
    'PXL_20261024_231405953.NIGHT.jpg': ('Reykjavík Harbor Aurora', 'Reykjavík Waterfront'),

    # Golden Circle
    'PXL_20261021_134158533.jpg': ('Þingvellir Rift Valley Entrance', 'Þingvellir National Park'),
    'PXL_20261021_150554681.jpg': ('Geysir Geothermal Basin', 'Haukadalur Valley'),
    'PXL_20261021_150901402.jpg': ('Strokkur Eruption', 'Geysir Geothermal Area'),
    'PXL_20261021_160006512.jpg': ('Gullfoss Canyon View', 'Gullfoss Canyon'),
    'PXL_20261021_161448972.jpg': ('Gullfoss Golden Waterfall', 'Gullfoss Canyon'),

    # Reykjavík Landmarks
    'PXL_20261022_101624879~2.jpg': ('Reykjavík Harbor Street', 'Reykjavík Downtown'),
    'PXL_20261022_113959206.jpg': ('Hallgrímskirkja Tower', 'Hallgrímskirkja • Reykjavík'),
    'PXL_20261026_163647963.jpg': ('Harpa Concert Hall Glass Facade', 'Harpa • Reykjavík Harbor'),
    'PXL_20261028_154753043.jpg': ('17th-Century Woodcarvings (Galdramenn)', 'National Museum of Iceland (Þjóðminjasafn Íslands)'),

    # Scuba Dives (Calibrated to 7 pure underwater dive shots)
    'IMG_4552.JPG': ('Descent into Continental Rift', 'Silfra Fissure (Dive 1)'),
    'IMG_4557.JPG': ('Glacial Water 100m Visibility', 'Silfra Fissure (Dive 1)'),
    'IMG_4582.JPG': ('Between Two Continents', 'Silfra Fissure (Dive 1)'),
    'IMG_4590.JPG': ('Silfra Hall & Light Beams', 'Silfra Fissure (Dive 1)'),
    'IMG_4616.JPG': ('Silfra Cathedral', 'Silfra Fissure (Dive 1)'),
    'IMG_4645.JPG': ('Silfra Lagoon Ascent', 'Silfra Lagoon (Dive 1)'),
    'IMG_4686.JPG': ('Davíðsgjá Deep Chasm', 'Davíðsgjá • Lake Þingvallavatn (Dive 2)'),

    # Glacier Lagoons & Diamond Beach
    'PXL_20261029_135850683.jpg': ('Diamond on Volcanic Black Sand', 'Diamond Beach'),
    'PXL_20261029_140727046.jpg': ('Glacial Ice Waves', 'Diamond Beach'),
    'PXL_20261029_142643385.jpg': ('Jökulsárlón Tidal Channel', 'Jökulsárlón Outlet'),
    'PXL_20261029_144743380.jpg': ('Floating Icebergs of Jökulsárlón', 'Jökulsárlón Glacier Lagoon'),
    'PXL_20261029_162555366.jpg': ('Glacial Meltwater Arch & Tunnel', 'En Route to Crystal Ice Cave • Vatnajökull'),
    'PXL_20261029_163623608.jpg': ('Glacier Lagoon Calving Ice Wall', 'Fjallsárlón Glacier Lagoon'),

    # Falljökull Ice Cave & South Coast
    'PXL_20261030_080318505.jpg': ('Southeast Coast Sunrise', 'Öræfi • Southeast Iceland'),
    'PXL_20261030_094030441.jpg': ('Falljökull Proglacial Lake & Ridge', 'Falljökull • Vatnajökull National Park'),
    'PXL_20261030_102016214.jpg': ('Glacier Hike Expedition', 'Falljökull • Vatnajökull National Park'),
    'PXL_20261030_103618991.jpg': ('Falljökull Ice Cave Portal Entrance', 'Falljökull • Vatnajökull National Park'),
    'PXL_20261030_104201790.jpg': ('Glacial Eye Arch Portal', 'Falljökull Ice Cave • Vatnajökull'),
    'PXL_20261030_104610152.jpg': ('Sculpted Glacial Ceiling', 'Falljökull Ice Cave • Vatnajökull'),
    'PXL_20261030_104911635.jpg': ('Sapphire Ice Chamber', 'Falljökull Ice Cave • Vatnajökull'),
    'PXL_20261030_144833807.jpg': ('Eldhraun Moss Lava Fields', 'Eldhraun Lava Field'),
    'PXL_20261030_155025285.jpg': ('Vík í Mýrdal Church & Coast', 'Vík í Mýrdal'),
    'PXL_20261030_163330009.jpg': ('Reynisfjara Black Sand Beach', 'Reynisfjara Beach'),
    'PXL_20261030_173120852.jpg': ('Skógafoss Waterfall', 'Skógar • South Coast'),
    'PXL_20261030_174357592.jpg': ('Skóga River Canyon', 'Skógá River'),
    'PXL_20261030_182033427.NIGHT.jpg': ('Seljalandsfoss Evening Mist', 'Seljalandsfoss Waterfall'),
    'PXL_20261030_183431300.NIGHT.jpg': ('Seljalandsfoss Night Illumination', 'Seljalandsfoss Waterfall'),

    # Snæfellsnes Peninsula & Conclusion
    'PXL_20261031_110103448.jpg': ('Kirkjufell Mountain', 'Grundarfjörður • Snæfellsnes'),
    'PXL_20261031_115324149~3.jpg': ('Ingjaldshólskirkja Church', 'Hellissandur • Snæfellsnes'),
    'PXL_20261031_123856453.jpg': ('Djúpalónssandur Beach & Epine Trawler Wreck', 'Djúpalónssandur • Snæfellsnes'),
    'PXL_20261031_132850938.jpg': ('Lóndrangar Basalt Pinnacles', 'Lóndrangar • Snæfellsnes'),
    'PXL_20261031_140732367.jpg': ('Gatklettur Natural Sea Arch', 'Arnarstapi Coast'),
    'PXL_20261031_142536925.jpg': ('Arnarstapi Cliff Walk', 'Arnarstapi Coastal Trail'),
    'PXL_20261031_150329519.jpg': ('Búðakirkja Black Church', 'Búðir • Snæfellsnes'),
    'PXL_20261031_154042672.jpg': ('Snæfellsnes Mountain Ridge', 'Snæfellsnes Peninsula'),
    'PXL_20261031_211327423.jpg': ('Farewell Night Over City', 'Reykjavík')
}

def dms_to_deg(dms, ref):
    if not dms: return None
    try:
        deg = float(dms[0])
        minute = float(dms[1])
        sec = float(dms[2])
        dec = deg + minute / 60.0 + sec / 3600.0
        if ref in ['S', 'W']: dec = -dec
        return round(dec, 6)
    except Exception:
        return None

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

def build():
    # Purge old folders
    if os.path.exists(THUMBS_DIR): shutil.rmtree(THUMBS_DIR)
    if os.path.exists(PHOTOS_DIR): shutil.rmtree(PHOTOS_DIR)
    os.makedirs(THUMBS_DIR, exist_ok=True)
    os.makedirs(PHOTOS_DIR, exist_ok=True)

    photos = []
    for fname, (title, place) in JOURNEY_ALLOWED.items():
        src_path = find_file(fname)
        if not src_path:
            print(f"Skipping {fname} (not found)")
            continue

        base_name, _ = os.path.splitext(fname)
        web_name = f"{base_name}.jpg"
        full_dest = os.path.join(PHOTOS_DIR, web_name)
        thumb_dest = os.path.join(THUMBS_DIR, web_name)

        shutil.copy2(src_path, full_dest)

        img = Image.open(src_path)
        w, h = img.size
        exif = img.getexif()
        exif_ifd = exif.get_ifd(0x8769) if exif else None
        gps_ifd = exif.get_ifd(0x8825) if exif else None
        dt_str = (exif_ifd.get(36867) or exif_ifd.get(36868) or exif.get(306)) if exif_ifd else exif.get(306)

        # Thumbnail
        thumb_img = ImageOps.exif_transpose(img)
        thumb_img.thumbnail((720, 720), Image.Resampling.LANCZOS)
        if thumb_img.mode in ('RGBA', 'P'):
            thumb_img = thumb_img.convert('RGB')
        thumb_img.save(thumb_dest, 'JPEG', quality=84, optimize=True)

        # GPS
        lat = lon = None
        if gps_ifd:
            lat = dms_to_deg(gps_ifd.get(2), gps_ifd.get(1))
            lon = dms_to_deg(gps_ifd.get(4), gps_ifd.get(3))

        # True dive anchors
        if lat is None:
            if 'Silfra' in place:
                lat, lon = COORDS_SILFRA
            elif 'Davíðsgjá' in place or 'David' in place:
                lat, lon = COORDS_DAVID

        is_hero = fname in HERO_SELECTION

        photos.append({
            'filename': fname,
            'title': title,
            'place': place,
            'is_hero': is_hero,
            'datetime': dt_str or '',
            'date_display': format_date_display(dt_str),
            'lat': lat,
            'lon': lon,
            'thumb': f"thumbs/{web_name}",
            'src': f"photos/{web_name}",
            'aspect': round(w / h, 3) if h else 1.5
        })

    # Sort strictly chronologically
    for p in photos:
        if p['datetime'].startswith('2023:11:03'):
            p['sort_key'] = p['datetime'].replace('2023:11:03', '2026:10:27')
        else:
            p['sort_key'] = p['datetime']

    photos.sort(key=lambda x: (x['sort_key'], x['filename']))
    for p in photos:
        del p['sort_key']

    with open(os.path.join(OUTPUT_DIR, 'data.json'), 'w', encoding='utf-8') as f:
        json.dump(photos, f, indent=2, ensure_ascii=False)

    heroes = sum(1 for p in photos if p['is_hero'])
    print(f"Build complete: {len(photos)} curated photos total. Heroes: {heroes}.")

if __name__ == '__main__':
    build()
