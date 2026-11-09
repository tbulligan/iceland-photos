import os, sys, json, hashlib, shutil
from PIL import Image, ImageOps

SOURCE_DIR = '/mnt/c/Users/tomas/Pictures/2026-Islanda'
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
THUMBS_DIR = os.path.join(OUTPUT_DIR, 'thumbs')
PHOTOS_DIR = os.path.join(OUTPUT_DIR, 'photos')

# Anchor coordinates for dive sites
COORDS_SILFRA = (64.25643, -21.11661)
COORDS_DAVID = (64.23617, -21.04493)

FALLBACK_COORDS = {
    '77033.jpg': (65.78125, -21.51889),
    '76752.jpg': (65.78093, -21.51894),
    '77436.jpg': (65.78093, -21.51894),
    'IMG_4188.jpeg': (65.78229, -21.49988),
    '1000089008.jpg': (64.14480, -21.93040),
    '_DSC0296.JPG': (65.78300, -21.51500),
    '1000226438.jpg': (65.78200, -21.51600),
    '1000226951.jpg': (65.70610, -21.66670),
    'PXL_20261023_214917931.jpg': (64.14032, -21.89969),
    '50e9e03c-63fc-42ea-80c6-3a3f112098fb.jpg': (64.14500, -21.93000),
    'IMG_5644.jpeg': (65.78200, -21.49800),
}

FALLBACK_DATETIME = {
    '50e9e03c-63fc-42ea-80c6-3a3f112098fb.jpg': '2026:10:24 12:00:00',
}

# 23 HIGHLIGHT HEROES (Every key milestone & trip climax)
HERO_SELECTION = {
    # Westfjords & Northern Lights
    '77033.jpg': ('YOIK Choir on the Strandir Coast', 'Drangsnes • Westfjords'),
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
    'PXL_20261029_144743380.jpg': ('Sculpted Blue Iceberg Arch', 'Jökulsárlón Glacier Lagoon'),
    'PXL_20261029_163623608.jpg': ('Glacier Lagoon Calving Ice Wall', 'Fjallsárlón Glacier Lagoon'),
    # Falljökull Ice Cave (Vatnajökull)
    'PXL_20261030_104201790.jpg': ('Glacial Eye Arch Portal', 'Falljökull Ice Cave • Vatnajökull'),
    'PXL_20261030_104911635.jpg': ('Sapphire Ice Chamber', 'Falljökull Ice Cave • Vatnajökull'),
    # South Coast
    'PXL_20261030_144641655.jpg': ('Embracing the Rapids of Foss á Síðu', 'Kirkjubæjarklaustur • South Coast'),
    'PXL_20261030_163330009.jpg': ('Reynisfjara Black Sand Beach', 'Reynisfjara Beach'),
    'PXL_20261030_173120852.jpg': ('Skógafoss Waterfall', 'Skógar • South Coast'),
    'PXL_20261030_183431300.NIGHT.jpg': ('Seljalandsfoss Night Illumination', 'Seljalandsfoss Waterfall'),
    # Snæfellsnes Peninsula
    'PXL_20261031_105933217.jpg': ('Kirkjufell & Kirkjufellsfoss', 'Grundarfjörður • Snæfellsnes'),
    'PXL_20261031_123856453.jpg': ('Djúpalónssandur Beach & Epine Trawler Wreck', 'Djúpalónssandur • Snæfellsnes'),
    'PXL_20261031_132850938.jpg': ('Lóndrangar Basalt Pinnacles', 'Lóndrangar • Snæfellsnes'),
    'PXL_20261031_140732367.jpg': ('Gatklettur Natural Sea Arch', 'Arnarstapi Coast'),
    'PXL_20261031_150329519.jpg': ('Búðakirkja Black Church', 'Búðir • Snæfellsnes'),
}

# EXACTLY 100 CURATED PHOTOS (Authentic travel narrative, ensemble, solo & highlights)
JOURNEY_ALLOWED = {
    # Oct 18 - 21: Strandir & Westfjords with YOIK Choir
    'PXL_20261018_085524369.jpg': ('Laugarhóll Valley Sunrise & Turf Shed', 'Bjarnarfjörður • Westfjords'),
    'PXL_20261018_111649700.jpg': ('Bjarnarfjörður Canyon Waterfall', 'Bjarnarfjörður • Westfjords'),
    'IMG_4188.jpeg': ('Weatherproof Hiking Squad', 'Bjarnarfjörður Canyon • Westfjords'),
    'IMG_5644.jpeg': ('Drangsnes Geothermal Hot Tubs with YOIK', 'Drangsnes • Westfjords'),
    '76752.jpg': ('YOIK Rehearsal at the Laugarhóll', 'Bjarnarfjörður • Westfjords'),
    '77033.jpg': ('YOIK Choir on the Strandir Coast', 'Drangsnes • Westfjords'),
    '1000226438.jpg': ('Coastal Ridge Walk', 'Drangsnes • Westfjords'),
    '_DSC0296.JPG': ('Ascending Above Steingrímsfjörður', 'Drangsnes • Westfjords'),
    '1000226951.jpg': ('Museum of Icelandic Sorcery & Witchcraft', 'Hólmavík • Westfjords'),
    'PXL_20261020_145812108.jpg': ('The Tilberi (Icelandic Sorcery Creature)', 'Museum of Witchcraft • Hólmavík'),
    'PXL_20261020_152145792.jpg': ('Hólmavíkurkirkja over Steingrímsfjörður', 'Hólmavík • Westfjords'),
    'PXL_20261020_152435767~2.jpg': ('Strandir Coast Sea Cliffs', 'Strandir Coast • Westfjords'),
    'PXL_20261020_223127604.NIGHT.jpg': ('First Aurora Glow', 'Drangsnes Sky • Westfjords'),
    '77436.jpg': ('Under the Northern Lights', 'Drangsnes • Westfjords'),
    'PXL_20261020_230151948.NIGHT.jpg': ('Northern Lights Curtain', 'Drangsnes • Westfjords'),
    'PXL_20261020_230341065.NIGHT.jpg': ('Emerald Aurora Swirl', 'Drangsnes • Westfjords'),
    'PXL_20261020_230644730.NIGHT.jpg': ('Aurora Over the Fjord', 'Strandir Coast'),
    'PXL_20261020_230907609.NIGHT.jpg': ('Corona Explosion', 'Drangsnes • Westfjords'),
    'PXL_20261021_081252444.jpg': ('Strandir Valley Autumn Frost', 'Drangsnes • Westfjords'),
    'PXL_20261021_091653823.jpg': ('Mountain Pass Descent', 'Westfjords Mountain Route'),

    # Oct 21: Golden Circle
    'PXL_20261021_134158533.jpg': ('Lake Þingvallavatn Overlook', 'Skálabrekka • Lake Þingvallavatn'),
    'PXL_20261021_150554681.jpg': ('Geysir Geothermal Basin', 'Haukadalur Valley'),
    'PXL_20261021_150901402.jpg': ('Strokkur Eruption', 'Geysir Geothermal Area'),
    'PXL_20261021_160006512.jpg': ('Gullfoss Canyon View', 'Gullfoss Canyon'),
    'PXL_20261021_161448972.jpg': ('Gullfoss Golden Waterfall', 'Gullfoss Canyon'),

    # Oct 21 - 26: Reykjavík & Lava Show
    'PXL_20261021_235716125.jpg': ('Hallgrímskirkja Violet Illumination', 'Hallgrímskirkja • Reykjavík'),
    'PXL_20261022_095104303.jpg': ('B47 Hostel Orchestra', 'Reykjavík'),
    'PXL_20261022_101624879~2.jpg': ('Hallgrímskirkja Grand Pipe Organ', 'Hallgrímskirkja • Reykjavík'),
    'PXL_20261022_113959206.jpg': ('Harpa Concert Hall Geometric Interior', 'Harpa • Reykjavík Harbor'),
    '1000089008.jpg': ('The YOIK Side of the Moon', 'Skólavörðustígur • Reykjavík'),
    'PXL_20261022_215442711.NIGHT.jpg': ('Reykjavík Aurora Borealis Vortex', 'Reykjavík Night Sky'),
    'PXL_20261023_214917931.jpg': ('YOIK-Huldur Gathering at RVK Brewing Co.', 'RVK Brewing Co. • Reykjavík'),
    '50e9e03c-63fc-42ea-80c6-3a3f112098fb.jpg': ('Emma: Host, Former Flatmate & Adventure Benefactor', 'Reykjavík'),
    'PXL_20261025_154614300.jpg': ('Fríkirkjan í Reykjavík by the Tjörnin', 'Tjörnin • Reykjavík'),
    'PXL_20261025_185719775.jpg': ('Salted Liquorice & Rye Bread Ice Cream', 'Valdís • Grandi • Reykjavík'),
    'PXL_20261025_215951062.jpg': ('Hostage to Sofía & Friðurfinnari', 'Reykjavík'),
    'PXL_20261026_161203144.jpg': ('Master of Molten Rock', 'Icelandic Lava Show • Reykjavík'),
    'PXL_20261026_162737009.jpg': ('Pouring 1100°C Liquid Basalt', 'Icelandic Lava Show • Reykjavík'),
    'PXL_20261026_163647963.jpg': ('Cooling Molten Lava Flow', 'Icelandic Lava Show • Reykjavík'),

    # Oct 27 - 28: DIVE.IS Silfra & Davíðsgjá Combo, and Reykjavík
    'IMG_4552.JPG': ('Descent into Continental Rift', 'Silfra Fissure (Dive 1)'),
    'IMG_4557.JPG': ('Silfra Entry Platform with Werner', 'Silfra Fissure • Þingvellir'),
    'IMG_4582.JPG': ('Between Two Continents', 'Silfra Fissure (Dive 1)'),
    'IMG_4590.JPG': ('Silfra Hall & Light Beams', 'Silfra Fissure (Dive 1)'),
    'IMG_4616.JPG': ('Silfra Cathedral', 'Silfra Fissure (Dive 1)'),
    'IMG_4645.JPG': ('Silfra Lagoon Ascent', 'Silfra Lagoon (Dive 1)'),
    'PXL_20261027_130347123.jpg': ('Langjökull Glacial Source & Mossy Lava Fields', 'Þingvellir National Park'),
    'PXL_20261027_151157243.jpg': ('Post-Dive Trio: Alex, Werner & Tomaso', 'Davíðsgjá • Lake Þingvallavatn'),
    'IMG_4686.JPG': ('Davíðsgjá Deep Chasm', 'Davíðsgjá • Lake Þingvallavatn (Dive 2)'),
    'IMG_4711.JPG': ('Davíðsgjá Basalt Fissure Hover', 'Davíðsgjá • Lake Þingvallavatn (Dive 2)'),
    'PXL_20261027_212539717.jpg': ('RVK Brewing Co. Happy Hour', 'RVK Brewing Co. • Reykjavík'),
    'PXL_20261028_122746447.jpg': ('Rainbow over Faxaflói Bay and Mount Esja', 'Sóltún • Reykjavík'),
    'PXL_20261028_142124937.jpg': ('Medieval Stave Church Carved Pillar', 'National Museum of Iceland'),
    'PXL_20261028_143748446.jpg': ('Valþjófsstaður Medieval Carved Chest', 'National Museum of Iceland'),
    'PXL_20261028_154753043.jpg': ('17th-Century Woodcarvings (Galdramenn)', 'National Museum of Iceland (Þjóðminjasafn Íslands)'),
    'PXL_20261028_175708712.jpg': ('Sun Voyager (Sólfar) under the Moon', 'Sæbraut • Reykjavík'),
    'PXL_20261028_181128651.jpg': ('Reykjavík Harbour Yellow Lighthouse', 'Reykjavík Harbour'),

    # Oct 29: Tröll Expeditions 2-Day South Coast & Glacier Lagoons
    'PXL_20261029_135850683.jpg': ('Diamond on Volcanic Black Sand', 'Diamond Beach'),
    'PXL_20261029_142643385.jpg': ('Jökulsárlón Tidal Channel', 'Jökulsárlón Outlet'),
    'PXL_20261029_144743380.jpg': ('Sculpted Blue Iceberg Arch', 'Jökulsárlón Glacier Lagoon'),
    'PXL_20261029_162106798.jpg': ('Crystal Ice Cave Subterranean River', 'Crystal Ice Cave • Breiðamerkurjökull'),
    'PXL_20261029_162555366.jpg': ('Crystal Ice Cave Cathedral Portal', 'Crystal Ice Cave • Breiðamerkurjökull'),
    'PXL_20261029_162720896.jpg': ('Crystal Cave Tephra Layers & Fluted Ice', 'Vatnajökull Ice Cave'),
    'PXL_20261029_163623608.jpg': ('Glacier Lagoon Calving Ice Wall', 'Fjallsárlón Glacier Lagoon'),
    'PXL_20261029_163826694.jpg': ('Fjallsárlón Calving Glacier Tongue', 'Fjallsárlón Glacier Lagoon'),

    # Oct 30: Tröll Expeditions Falljökull Ice Cave & South Coast Waterfalls
    'PXL_20261030_080318505.jpg': ('Southeast Coast Sunrise', 'Öræfi • Southeast Iceland'),
    'PXL_20261030_093228132.jpg': ('Falljökull Proglacial Outwash Plain', 'Falljökull • Vatnajökull National Park'),
    'PXL_20261030_094030441.jpg': ('Falljökull Proglacial Lake & Ridge', 'Falljökull • Vatnajökull National Park'),
    'PXL_20261030_102016214.jpg': ('Glacier Hike Expedition', 'Falljökull • Vatnajökull National Park'),
    'PXL_20261030_102417128.jpg': ('Falljökull Glacier Crevasse Field', 'Falljökull • Vatnajökull'),
    'PXL_20261030_103618991.jpg': ('Falljökull Ice Cave Portal Entrance', 'Falljökull • Vatnajökull National Park'),
    'PXL_20261030_104201790.jpg': ('Glacial Eye Arch Portal', 'Falljökull Ice Cave • Vatnajökull'),
    'PXL_20261030_104610152.jpg': ('Sculpted Glacial Ceiling', 'Falljökull Ice Cave • Vatnajökull'),
    'PXL_20261030_104911635.jpg': ('Sapphire Ice Chamber', 'Falljökull Ice Cave • Vatnajökull'),
    'PXL_20261030_111446663.jpg': ('On Falljökull Glacier', 'Falljökull • Vatnajökull National Park'),
    'PXL_20261030_113703709.jpg': ('Thumbs Up at the Falljökull Icefall', 'Falljökull • Vatnajökull National Park'),
    'PXL_20261030_144641655.jpg': ('Embracing the Rapids of Foss á Síðu', 'Kirkjubæjarklaustur • South Coast'),
    'PXL_20261030_155025285.jpg': ('Vík í Mýrdal Graveyard & Mountains', 'Vík í Mýrdal'),
    'PXL_20261030_155507298.jpg': ('Reynisdrangar Sea Stacks from Vík', 'Vík í Mýrdal'),
    'PXL_20261030_163330009.jpg': ('Reynisfjara Black Sand Beach', 'Reynisfjara Beach'),
    'PXL_20261030_173120852.jpg': ('Skógafoss Waterfall', 'Skógar • South Coast'),
    'PXL_20261030_174141238.jpg': ('Skógafoss Vertical Canyon Plunge', 'Skógar • South Coast'),
    'PXL_20261030_182322356.NIGHT.jpg': ('Cavern Passage Behind Seljalandsfoss', 'Seljalandsfoss Waterfall'),
    'PXL_20261030_183431300.NIGHT.jpg': ('Seljalandsfoss Night Illumination', 'Seljalandsfoss Waterfall'),

    # Oct 31: Tröll Expeditions Snæfellsnes Peninsula Tour & Farewell
    'PXL_20261031_105933217.jpg': ('Kirkjufell & Kirkjufellsfoss', 'Grundarfjörður • Snæfellsnes'),
    'PXL_20261031_115324149~3.jpg': ('Ingjaldshólskirkja Church', 'Hellissandur • Snæfellsnes'),
    'PXL_20261031_123419469.jpg': ('Djúpalónssandur Black Pebble Cove', 'Djúpalónssandur • Snæfellsnes'),
    'PXL_20261031_123856453.jpg': ('Djúpalónssandur Beach & Epine Trawler Wreck', 'Djúpalónssandur • Snæfellsnes'),
    'PXL_20261031_124528772.jpg': ('Djúpalónssandur Sea Stacks & Sunburst', 'Djúpalónssandur • Snæfellsnes'),
    'PXL_20261031_124833938.jpg': ('Djúpalónssandur Volcanic Monoliths', 'Djúpalónssandur • Snæfellsnes'),
    'PXL_20261031_130448667.jpg': ('Embracing the Elements at Djúpalónssandur', 'Djúpalónssandur • Snæfellsnes'),
    'PXL_20261031_132850938.jpg': ('Lóndrangar Basalt Pinnacles', 'Lóndrangar • Snæfellsnes'),
    'PXL_20261031_133314715.jpg': ('Lóndrangar Ocean Promontory & Rain Squall', 'Lóndrangar • Snæfellsnes'),
    'PXL_20261031_133833097.jpg': ('Svalþúfa Sea Cliff Trail', 'Lóndrangar • Snæfellsnes'),
    'PXL_20261031_140115572.jpg': ('Arnarstapi Roaring Sea Blowhole', 'Arnarstapi Coast'),
    'PXL_20261031_140732367.jpg': ('Gatklettur Natural Sea Arch', 'Arnarstapi Coast'),
    'PXL_20261031_142536925.jpg': ('Arnarstapi Cliff Walk', 'Arnarstapi Coastal Trail'),
    'PXL_20261031_150329519.jpg': ('Búðakirkja Black Church', 'Búðir • Snæfellsnes'),
    'PXL_20261031_153459957.jpg': ('Ytri-Tunga Seal Colony... Allegedly :)', 'Ytri-Tunga • Snæfellsnes'),
    'PXL_20261031_154042672.jpg': ('Snæfellsnes Mountain Ridge', 'Snæfellsnes Peninsula'),
    'PXL_20261031_211327423.jpg': ('Farewell, Þorsteinn and Ingibjörg!', 'Reykjavík'),
}

def dms_to_deg(dms, ref):
    if not dms or len(dms) < 3: return None
    try:
        def to_f(v):
            if hasattr(v, 'numerator') and hasattr(v, 'denominator'):
                return float(v.numerator) / float(v.denominator) if v.denominator != 0 else 0.0
            return float(v)
        deg = to_f(dms[0])
        minute = to_f(dms[1])
        sec = to_f(dms[2])
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
    p1 = os.path.join(SOURCE_DIR, fname)
    if os.path.isfile(p1): return p1
    p2 = os.path.join(SOURCE_DIR, 'with-me-from-others', fname)
    if os.path.isfile(p2): return p2
    for sub in ['Dives', 'Dive 1', 'Dive 2', 'Silfra', 'David']:
        p3 = os.path.join(SOURCE_DIR, sub, fname)
        if os.path.isfile(p3): return p3
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

        img = Image.open(src_path)
        exif = img.getexif()
        exif_ifd = exif.get_ifd(0x8769) if exif else None
        gps_ifd = exif.get_ifd(0x8825) if exif else None
        dt_str = (exif_ifd.get(36867) or exif_ifd.get(36868) or exif.get(306)) if exif_ifd else (exif.get(306) if exif else None)
        if not dt_str and fname in FALLBACK_DATETIME:
            dt_str = FALLBACK_DATETIME[fname]

        # Full photo with correct orientation
        transposed_img = ImageOps.exif_transpose(img)
        w, h = transposed_img.size
        orient = exif.get(0x0112) if exif else 1
        if orient in (None, 1):
            shutil.copy2(src_path, full_dest)
        else:
            save_exif = img.getexif()
            save_exif[0x0112] = 1
            full_img = transposed_img
            if max(w, h) > 3840:
                scale = 3840.0 / max(w, h)
                full_img = full_img.resize((int(round(w * scale)), int(round(h * scale))), Image.Resampling.LANCZOS)
            if full_img.mode in ('RGBA', 'P'):
                full_img = full_img.convert('RGB')
            save_kwargs = {'quality': 85, 'subsampling': 2, 'exif': save_exif, 'optimize': True}
            if img.info.get('icc_profile'):
                save_kwargs['icc_profile'] = img.info['icc_profile']
            full_img.save(full_dest, 'JPEG', **save_kwargs)

        # Thumbnail with correct EXIF orientation
        thumb_img = transposed_img.copy()
        thumb_img.thumbnail((720, 720), Image.Resampling.LANCZOS)
        if thumb_img.mode in ('RGBA', 'P'):
            thumb_img = thumb_img.convert('RGB')
        thumb_img.save(thumb_dest, 'JPEG', quality=84, optimize=True)

        # GPS coordinates
        lat = lon = None
        if gps_ifd:
            lat = dms_to_deg(gps_ifd.get(2), gps_ifd.get(1))
            lon = dms_to_deg(gps_ifd.get(4), gps_ifd.get(3))

        # True dive & location fallbacks
        if lat is None or lon is None or (lat == 0.0 and lon == 0.0):
            if 'Silfra' in place:
                lat, lon = COORDS_SILFRA
            elif 'Davíðsgjá' in place or 'David' in place:
                lat, lon = COORDS_DAVID
            elif fname in FALLBACK_COORDS:
                lat, lon = FALLBACK_COORDS[fname]

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

    with open(os.path.join(OUTPUT_DIR, 'data.js'), 'w', encoding='utf-8') as f:
        f.write('window.ALL_PHOTOS = ' + json.dumps(photos, indent=2, ensure_ascii=False) + ';\n')

    heroes = sum(1 for p in photos if p['is_hero'])
    print(f"Build complete: {len(photos)} curated photos total. Heroes: {heroes}.")

if __name__ == '__main__':
    build()
