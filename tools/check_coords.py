import urllib.request, json

# Let's reverse geocode or check landmarks near the coords
coords = [
    (64.14191, -21.94834, "Oct 28 Museum"),
    (64.04331, -16.17531, "Oct 29 13:58 Diamond Beach"),
    (64.04889, -16.18069, "Oct 29 14:47 Jokulsarlon"),
    (64.09505, -16.33366, "Oct 29 15:39 Moraine/Fjallsarlon?"),
    (64.09891, -16.30318, "Oct 29 16:25 Ice arch / cave"),
    (64.09870, -16.30197, "Oct 29 16:36 Lagoon/Ice wall"),
    (63.97284, -16.80607, "Oct 30 10:36 Ice cave entry"),
    (63.97263, -16.80614, "Oct 30 10:49 Inside blue ice cave"),
    (63.97339, -16.80029, "Oct 30 11:37 Tomaso glacier thumbs up"),
    (63.85256, -17.83948, "Oct 30 14:48 Eldhraun"),
    (63.42178, -19.00102, "Oct 30 15:50 Vik"),
    (63.40324, -19.04411, "Oct 30 16:33 Reynisfjara"),
    (63.53182, -19.51074, "Oct 30 17:31 Skogafoss"),
    (63.61553, -19.98940, "Oct 30 18:20 Seljalandsfoss"),
    (64.75343, -23.89981, "Oct 31 12:38 Djupalonssandur"),
    (64.73523, -23.77415, "Oct 31 13:33 Londrangar"),
    (64.76550, -23.62219, "Oct 31 14:07 Arnarstapi Gatklettur"),
]

for lat, lon, desc in coords:
    print(f"{lat}, {lon} -> {desc}")
