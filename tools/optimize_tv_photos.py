import os, glob
from PIL import Image, ImageOps

PHOTOS_DIR = os.path.abspath('photos')

def optimize_all():
    files = sorted(glob.glob(os.path.join(PHOTOS_DIR, '*')))
    total_before = 0
    total_after = 0
    processed = 0

    for path in files:
        base = os.path.basename(path)
        if base.startswith('PXL_'):
            continue  # Keep original Pixel photos with Ultra HDR untouched
        
        orig_bytes = os.path.getsize(path)
        with Image.open(path) as img:
            w, h = img.size
            max_dim = max(w, h)
            needs_resize = (max_dim > 3840)
            needs_reencode = (orig_bytes > 1.8 * 1024 * 1024)

            if not needs_resize and not needs_reencode:
                continue

            transposed = ImageOps.exif_transpose(img)
            tw, th = transposed.size

            if max(tw, th) > 3840:
                scale = 3840.0 / max(tw, th)
                new_size = (int(round(tw * scale)), int(round(th * scale)))
                resample = getattr(Image.Resampling, 'LANCZOS', Image.LANCZOS)
                out_img = transposed.resize(new_size, resample)
            else:
                out_img = transposed.copy()
                new_size = (tw, th)

            if out_img.mode in ('RGBA', 'P'):
                out_img = out_img.convert('RGB')

            exif = img.getexif()
            exif[0x0112] = 1 # upright

            save_kwargs = {
                'quality': 85,
                'subsampling': 2,
                'exif': exif,
                'optimize': True
            }
            if img.info.get('icc_profile'):
                save_kwargs['icc_profile'] = img.info['icc_profile']

            tmp_path = path + '.opt.jpg'
            out_img.save(tmp_path, 'JPEG', **save_kwargs)

        new_bytes = os.path.getsize(tmp_path)
        os.replace(tmp_path, path)

        total_before += orig_bytes
        total_after += new_bytes
        processed += 1
        pct = 100 * (1 - new_bytes / orig_bytes)
        print(f"{base:22s}: ({w}x{h}) {orig_bytes/1e6:5.2f}MB -> ({new_size[0]}x{new_size[1]}) {new_bytes/1e6:5.2f}MB (-{pct:4.1f}%)")

    print(f"\nFinished: {processed} photos optimized.")
    print(f"Total payload: {total_before/1e6:.2f}MB -> {total_after/1e6:.2f}MB (Saved {(total_before-total_after)/1e6:.2f}MB, -{100*(1-total_after/total_before):.1f}%)")

if __name__ == '__main__':
    optimize_all()
