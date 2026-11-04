import os, sys
sys.path.append('/home/tomaso/projects/iceland-photos')
from PIL import Image
from build_album import HERO_SELECTION, JOURNEY_ALLOWED

SOURCE = '/mnt/c/Users/tomas/Pictures/2026-Islanda'

print(f"HERO COUNT: {len(HERO_SELECTION)}")
print(f"JOURNEY COUNT: {len(JOURNEY_ALLOWED)}")

all_keys = list(HERO_SELECTION.keys()) + [k for k in JOURNEY_ALLOWED if k not in HERO_SELECTION]
print(f"UNIQUE TOTAL: {len(all_keys)}")

for k in all_keys:
    p = None
    for root, dirs, files in os.walk(SOURCE):
        if k in files:
            p = os.path.join(root, k)
            break
    if not p:
        print(f"MISSING: {k}")
    else:
        title, place = HERO_SELECTION.get(k) or JOURNEY_ALLOWED.get(k)
        is_hero = "HERO" if k in HERO_SELECTION else "    "
        print(f"[{is_hero}] {k} -> [{title}] | [{place}]")
