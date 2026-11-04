"""places.py의 장소 중 좌표(ll)가 없는 것을 Nominatim으로 지오코딩해 coords.json에 저장한다."""
import json
import os
import ssl
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from places import PLACES  # noqa: E402

OUT = sys.argv[1]
UA = "SpainTripMapBuilder/1.0"
CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
coords = json.load(open(OUT)) if os.path.exists(OUT) else {}

for key, place in PLACES.items():
    if key in coords:
        continue
    if "ll" in place:
        coords[key] = {"lat": place["ll"][0], "lon": place["ll"][1], "src": "manual"}
        continue
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({"q": place["q"], "format": "json", "limit": 1})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
            hits = json.loads(r.read())
        if hits:
            coords[key] = {"lat": float(hits[0]["lat"]), "lon": float(hits[0]["lon"]), "src": hits[0]["display_name"][:80]}
            print(key, "OK", coords[key]["src"], flush=True)
        else:
            print(key, "NO HIT", place["q"], flush=True)
    except Exception as e:
        print(key, "ERR", e, flush=True)
    time.sleep(1.2)  # Nominatim 사용 정책: 초당 1회 이하

json.dump(coords, open(OUT, "w"), ensure_ascii=False, indent=1)
print(len(coords), "coords")
