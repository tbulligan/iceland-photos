import os
from PIL import Image

TARGETS = [
    'photos/77436.jpg',
    'photos/IMG_4188.jpg'
]

def optimize_file(rel_path, max_dim=3840, quality=85):
    path = os.path.abspath(rel_path)
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return

    with Image.open(path) as img:
        orig_size = img.size
        orig_bytes = os.path.getsize(path)
        w, h = orig_size
        
        # Scale to max dimension 3840 if larger (matching rest of 4K album)
        if max(w, h) > max_dim:
            scale = max_dim / float(max(w, h))
            new_size = (int(round(w * scale)), int(round(h * scale)))
            resample_filter = getattr(Image.Resampling, 'LANCZOS', Image.LANCZOS)
            out_img = img.resize(new_size, resample_filter)
        else:
            out_img = img.copy()
            new_size = orig_size

        if out_img.mode in ('RGBA', 'P'):
            out_img = out_img.convert('RGB')

        exif = img.getexif()
        exif[0x0112] = 1 # upright

        tmp_path = path + ".opt.jpg"
        # quality=85 + subsampling=2 (4:2:0) enables TV hardware JPEG decoder
        out_img.save(
            tmp_path,
            "JPEG",
            quality=quality,
            subsampling=2,
            exif=exif,
            optimize=True
        )

    new_bytes = os.path.getsize(tmp_path)
    os.replace(tmp_path, path)
    
    print(f"{rel_path}: {orig_size} ({orig_bytes/1e6:.2f}MB) -> {new_size} ({new_bytes/1e6:.2f}MB), drop: {100*(1 - new_bytes/orig_bytes):.1f}%")

if __name__ == '__main__':
    for target in TARGETS:
        optimize_file(target)
