import urllib.request
import json
import time

coords = [
    ('Oct 29 15:39', 64.09505, -16.33366),
    ('Oct 29 16:25', 64.09891, -16.30318),
    ('Oct 29 16:36', 64.09870, -16.30197),
    ('Oct 30 08:03', 64.12872, -16.01139),
    ('Oct 30 09:40', 63.96510, -16.80712),
    ('Oct 30 10:20', 63.97164, -16.80411),
    ('Oct 30 10:36', 63.97284, -16.80607),
    ('Oct 30 10:49', 63.97263, -16.80614),
    ('Oct 30 11:37', 63.97339, -16.80029),
    ('Oct 30 14:48', 63.85256, -17.83948),
    ('Oct 30 15:50', 63.42178, -19.00102),
    ('Oct 30 16:33', 63.40324, -19.04411),
    ('Oct 30 17:31', 63.53182, -19.51074),
    ('Oct 30 18:20', 63.61553, -19.98940),
    ('Oct 31 11:01', 64.92606, -23.31152),
    ('Oct 31 11:53', 64.90866, -23.85358),
    ('Oct 31 12:31', 64.75373, -23.89692),
    ('Oct 31 12:38', 64.75343, -23.89981),
    ('Oct 31 13:04', 64.75289, -23.89823),
    ('Oct 31 13:33', 64.73523, -23.77415),
    ('Oct 31 14:07', 64.76550, -23.62219),
    ('Oct 31 14:25', 64.77033, -23.61833),
    ('Oct 31 15:03', 64.82158, -23.38441),
    ('Oct 31 15:40', 64.80366, -23.08150),
]

for label, lat, lon in coords:
    # Use OpenStreetMap Nominatim reverse geocoding
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&zoom=14"
    req = urllib.request.Request(url, headers={'User-Agent': 'iceland-photo-curator/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            name = data.get('display_name', '')
            print(f"{label} ({lat}, {lon}) -> {name}")
    except Exception as e:
        print(f"{label} ({lat}, {lon}) -> error: {e}")
    time.sleep(1)
