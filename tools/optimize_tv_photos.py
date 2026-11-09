import os, subprocess, io
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

    # Extract original ICC profile from git if present
    icc = None
    try:
        blob = subprocess.check_output(['git', 'show', f'6ec769d:{rel_path}'])
        orig_git_im = Image.open(io.BytesIO(blob))
        icc = orig_git_im.info.get('icc_profile')
    except Exception as e:
        print(f"Warning extracting ICC: {e}")

    with Image.open(path) as img:
        orig_size = img.size
        w, h = orig_size
        
        # Scale to max dimension 3840 if larger
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
        save_kwargs = {
            'quality': quality,
            'subsampling': 2,
            'exif': exif,
            'optimize': True
        }
        if icc:
            save_kwargs['icc_profile'] = icc

        out_img.save(tmp_path, "JPEG", **save_kwargs)

    orig_bytes = os.path.getsize(path)
    new_bytes = os.path.getsize(tmp_path)
    os.replace(tmp_path, path)
    
    print(f"{rel_path}: {new_size} ({new_bytes/1e6:.2f}MB, ICC embedded={bool(icc)})")

if __name__ == '__main__':
    for target in TARGETS:
        optimize_file(target)
