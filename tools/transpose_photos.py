import os
from PIL import Image, ImageOps

PHOTOS = [
    'photos/77436.jpg',
    'photos/IMG_4188.jpg'
]

def main():
    for rel_path in PHOTOS:
        path = os.path.abspath(rel_path)
        if not os.path.exists(path):
            print(f"Not found: {path}")
            continue
        
        with Image.open(path) as img:
            exif = img.getexif()
            orient = exif.get(0x0112)
            orig_size = img.size
            print(f"Processing {rel_path}: size={orig_size}, orient={orient}")
            
            if orient in (None, 1):
                print(f"Skipping {rel_path} (already orient {orient})")
                continue
            
            transposed = ImageOps.exif_transpose(img)
            new_size = transposed.size
            
            # Reset EXIF orientation tag to 1
            exif[0x0112] = 1
            
            tmp_path = path + ".tmp.jpg"
            transposed.save(tmp_path, "JPEG", quality=95, exif=exif, optimize=True)
            
        os.replace(tmp_path, path)
        
        # Verify result
        with Image.open(path) as check_img:
            check_exif = check_img.getexif()
            print(f"Verified {rel_path}: size={check_img.size}, orient={check_exif.get(0x0112)}")

if __name__ == '__main__':
    main()
