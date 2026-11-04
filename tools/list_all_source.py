import os
from PIL import Image

SOURCE_DIR = '/mnt/c/Users/tomas/Pictures/2026-Islanda'

def check(f):
    p = os.path.join(SOURCE_DIR, f)
    if os.path.exists(p):
        im = Image.open(p)
        print(f"{f}: size={im.size}")

for f in sorted(os.listdir(SOURCE_DIR)):
    if f.endswith('.jpg'):
        print(f)
