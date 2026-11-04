import os

src_dir = '/mnt/c/Users/tomas/Pictures/2026-islanda-extra'
if os.path.exists(src_dir):
    files = sorted(os.listdir(src_dir))
    print(f'Total in extra: {len(files)}')
    for f in files:
        print(f)
else:
    print('Not found')
