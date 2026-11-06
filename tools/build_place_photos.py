"""일정의 명소·호텔 사진을 모아 data/<나라>/places.json 을 만든다. web/app.js 의 장소 카드·오늘 숙소, booking.html 숙소 항목이 읽는다.
사용: python -I tools/build_place_photos.py spain|greece|portugal|czech [--no-net]
- 명소: 위키미디어 커먼즈 (검색어는 places 의 q, 바꿀 때는 place_photo_q.py 의 Q)
- 호텔: 호텔 공식 사이트의 대표 사진(og:image). 없거나 막히면 커먼즈
- 식당(식당 카드가 따로 있음)은 건너뛴다. 역·공항·정류장도 사진을 넣는다
사진이 틀리면 photos/<나라>/places/<키>.jpg 와 credits.json 의 그 키를 지우고, place_photo_q.py 에 검색어를 적어 다시 돌린다."""
import html
import importlib.util
import json
import os
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import commons  # noqa: E402
from place_photo_q import Q, OFFICIAL, SKIP  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
K = sys.argv[1]
NET = "--no-net" not in sys.argv
DATA = os.path.join(ROOT, "data", "" if K == "spain" else K)
PDIR = os.path.join(ROOT, "photos", "" if K == "spain" else K, "places")
WEB = "photos/%splaces/" % ("" if K == "spain" else K + "/")
os.makedirs(PDIR, exist_ok=True)

if K == "spain":
    from places import PLACES  # noqa: E402
    from blobs import HOTEL_LINKS as HOTELS  # noqa: E402
    src = open(os.path.join(HERE, "build_booking.py"), encoding="utf-8").read()
    official = {}
    for k, (name, _, _) in HOTELS.items():  # build_booking.py 의 HOTEL_META 는 "이름" 키 — 공식 주소만 읽는다
        m = re.search(r'"%s": \{[^}]*"official": "([^"]+)"' % re.escape(name.split(" (")[0]), src)
        if m:
            official[k] = m.group(1)
else:
    spec = importlib.util.spec_from_file_location("trip", os.path.join(HERE, "countries", K, "trip.py"))
    trip = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(trip)
    PLACES, HOTELS = trip.PLACES, trip.HOTELS
    official = {k: m.get("official") for k, m in trip.HOTEL_META.items() if m.get("official")}
official.update(OFFICIAL.get(K, {}))

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
CTX = ssl.create_default_context()
BAD = re.compile(r"\bmap\b|plan\b|logo|coat of arms|wappen|stamp|diagram|drawing|engraving|lithograph|painting|postcard|"
                 r"\bsign\b|plaque|interior detail|ticket|\b1[5-8]\d\d\b|\b19[0-5]\d\b|document|scan", re.I)


def ok_photo(r):
    """가로 사진만 (너무 긴 파노라마도 빼고), 지도·그림·옛 엽서 같은 건 뺀다. ("File:" 로 직접 고른 사진은 commons.first 가 그대로 쓴다)"""
    return r["h"] * 1.15 <= r["w"] <= r["h"] * 2.1 and not BAD.search(r["title"])


# ───── 어떤 장소를 쓰나: courses.json 의 '장소' 행 이름 ↔ places 의 ko ─────
courses = json.load(open(os.path.join(DATA, "courses.json"), encoding="utf-8"))
rest = json.load(open(os.path.join(DATA, "restaurants.json"), encoding="utf-8")) if os.path.exists(os.path.join(DATA, "restaurants.json")) else {}
rest_match = [m for r in rest.values() for m in r["match"]]
by_ko = {}
for key, p in PLACES.items():
    by_ko.setdefault(p["ko"], key)
used, sleep_names = [], set()
for c in courses.values():
    for d in c["days"]:
        if d.get("sleepName"):
            sleep_names.add(d["sleepName"])
        for it in d["items"]:
            if it["kind"] != "stop":
                continue
            ko = re.sub(r"^\d+ ", "", it["head"])
            key = by_ko.get(ko)
            if key and key not in used:
                used.append(key)

targets = []
for key in used:
    ko = PLACES[key]["ko"]
    if key in HOTELS:
        targets.append((key, "hotel"))
    elif key in SKIP.get(K, ()) or any(ko.startswith(m) for m in rest_match):
        continue
    else:
        targets.append((key, "place"))
for hk, (hname, _, _) in HOTELS.items():  # 체크인 행이 없는 숙소도 '오늘 숙소'에 쓴다
    if hname in sleep_names and not any(k == hk for k, _ in targets):
        targets.append((hk, "hotel"))


def og_image(url):
    """공식 사이트 첫 화면의 og:image (호텔이 공유용으로 내건 대표 사진). 없으면 첫 화면의 첫 큰 사진."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html", "Accept-Language": "en"})
    with urllib.request.urlopen(req, timeout=25, context=CTX) as r:
        page = r.read(600000).decode("utf-8", "ignore")
        base = r.geturl()
    for pat in (r'<meta[^>]+property=["\']og:image(?::url)?["\'][^>]+content=["\']([^"\']+)',
                r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image',
                r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)'):
        m = re.search(pat, page, re.I)
        if m:
            return fix_url(urllib.parse.urljoin(base, html.unescape(m.group(1).strip())))
    for m in re.finditer(r'(?:src|href|data-src)=["\']([^"\']+\.(?:jpe?g|webp)[^"\']*)', page, re.I):
        if not re.search(r"logo|icon|badge|favicon|sprite", m.group(1), re.I):
            return fix_url(urllib.parse.urljoin(base, html.unescape(m.group(1))))
    return None


def fix_url(u):
    """주소 안의 한글·악센트 글자를 %인코딩 (Casa Mãe 처럼)."""
    return urllib.parse.quote(u, safe=":/?&=%#,;+@~")


def save_small(raw, fn, width=900):
    """사진을 가로 900px JPEG 로 줄여 저장 (공식 사이트 원본은 수 MB 라서)."""
    try:
        from io import BytesIO
        from PIL import Image
        img = Image.open(BytesIO(raw)).convert("RGB")
        if img.width < 400:
            return False
        if img.width > width:
            img = img.resize((width, round(img.height * width / img.width)))
        img.save(fn, "JPEG", quality=82, optimize=True)
        return True
    except Exception as e:
        print("  img ERR", e)
        return False


cred_path = os.path.join(PDIR, "credits.json")
cred = json.load(open(cred_path, encoding="utf-8")) if os.path.exists(cred_path) else {}
for key, kind in targets:
    fn = os.path.join(PDIR, key + ".jpg")
    if key in cred and os.path.exists(fn) or not NET:
        continue
    p = PLACES.get(key, {})
    got = None
    if kind == "hotel" and official.get(key):
        site, img = official[key] if isinstance(official[key], tuple) else (official[key], None)  # (사이트, 사진 주소) 로 직접 줄 수도 있다
        try:
            img = img or og_image(site)
            if img:
                req = urllib.request.Request(img, headers={"User-Agent": UA, "Referer": site, "Accept": "image/*"})
                with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
                    raw = r.read()
                if save_small(raw, fn):
                    got = {"src": "official", "page": site, "image": img, "artist": "호텔 공식 사이트", "license": ""}
        except Exception as e:
            print("  og ERR", key, e)
    if not got:
        # 호텔은 이름만 같은 엉뚱한 건물이 잡히기 쉬워서, 검색어를 직접 적은 경우에만 커먼즈를 쓴다
        qs = Q.get(K, {}).get(key) or ([] if kind == "hotel" else [p.get("q", ""), p.get("q", "").split(",")[0]])
        pick = commons.first([q for q in qs if q], width=900, ok=ok_photo)
        if pick:
            open(fn, "wb").write(commons.fetch(pick["thumb"]))
            got = dict(pick, src="commons")
        time.sleep(0.8)
    if got:
        got.update(kind=kind, ko=p.get("ko") or HOTELS[key][0])
        cred[key] = got
        print("ok  ", kind, key, got.get("title", got.get("image", ""))[:70], flush=True)
        json.dump(cred, open(cred_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    else:
        print("NONE", kind, key, p.get("ko", ""), flush=True)


# ───── places.json: 행 이름 → 사진, 숙소 이름 → 사진 ─────
def card(key):
    c = cred[key]
    credit = "사진: 호텔 공식 사이트" if c["src"] == "official" else "%s · %s · Wikimedia Commons" % (c["artist"], c["license"])
    return {"file": WEB + key + ".jpg", "kind": c["kind"], "credit": credit, "page": c["page"]}


out = {"places": {}, "hotels": {}}
for key, kind in targets:
    if key in cred and os.path.exists(os.path.join(PDIR, key + ".jpg")):
        if key in PLACES:
            out["places"][PLACES[key]["ko"]] = card(key)
        if kind == "hotel":
            out["hotels"][HOTELS[key][0]] = card(key)
json.dump(out, open(os.path.join(DATA, "places.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("%s: %d targets, %d places, %d hotels with photo" % (K, len(targets), len(out["places"]), len(out["hotels"])))
