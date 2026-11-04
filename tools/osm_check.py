import urllib.request, json

coords = [
    (64.14191, -21.94834),
    (64.09505, -16.33366),
    (64.09891, -16.30318),
    (63.97284, -16.80607),
    (63.96426, -16.80978),
]

for lat, lon in coords:
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=14"
    req = urllib.request.Request(url, headers={'User-Agent': 'IcelandPhotoChecker/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"{lat}, {lon} -> {data.get('display_name')}")
    except Exception as e:
        print(f"Error {lat}, {lon}: {e}")
