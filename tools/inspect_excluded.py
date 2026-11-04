import os, json

with open('data.json') as f:
    current = {p['filename'] for p in json.load(f)}

src_dir = '/mnt/c/Users/tomas/Pictures/2026-Islanda'
all_src = [f for f in os.listdir(src_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

not_included = [f for f in all_src if f not in current]
print(f'Total in 2026-Islanda: {len(all_src)}')
print(f'Included: {len(all_src) - len(not_included)}')
print(f'Not included: {len(not_included)}')

for f in sorted(not_included):
    print(f)
