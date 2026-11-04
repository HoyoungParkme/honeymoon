"""나라 하나의 웹 데이터를 만든다: tools/countries/<나라>/trip.py → data/<나라>/*.json + photos/<나라>/.
스페인(캔버스 보드가 딸린 원조 파이프라인)은 build_boards.py 를 쓰고, 새 나라는 이걸 쓴다.
사용: python -I tools/build_country.py greece [--no-net]   (--no-net: 지오코딩·경로·사진 내려받기 생략)

만드는 것
- courses.json  코스 × 날짜 × 행 (web/app.js 가 읽는 형식, 스페인과 같음)
- coords.json   장소 위경도 (places 의 ll 우선, 없으면 Nominatim)
- index.json    지도 구간 ↔ 행 번호 · 마커 번호 (열차·비행기·페리에서 구간을 나눈다)
- routes.json   도보 구간 실제 경로 (OSRM foot)
- budget.json   코스 선택 페이지 예산 막대
- booking.json  예약 체크리스트 (숙소는 잠자리에서 자동, 나머지는 trip.BOOKING)
- restaurants.json 식당 카드 (가게·대표 음식 사진 포함)"""
import importlib.util
import json
import os
import ssl
import sys
import time
import urllib.parse
import urllib.request
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from tripkit import MODE_KO, add_times, due_of, eur_of, shift  # noqa: E402
import commons  # noqa: E402

K = sys.argv[1]
NET = "--no-net" not in sys.argv
spec = importlib.util.spec_from_file_location("trip", os.path.join(HERE, "countries", K, "trip.py"))
trip = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trip)

OUT = os.path.join(ROOT, "data", K)
PHOTO_DIR = os.path.join(ROOT, "photos", K)
FOOD_DIR = os.path.join(PHOTO_DIR, "food")
for d in (OUT, PHOTO_DIR, FOOD_DIR):
    os.makedirs(d, exist_ok=True)
PLACES = trip.PLACES
COURSES = {c: [add_times(d) for d in days] for c, days in trip.COURSES.items()}
LONG_HAUL = {"train", "plane", "ferry"}
GMAP_MODE = {"walk": "walking", "taxi": "driving", "boat": "driving"}
UA = "HoneymoonTripBuilder/1.0"
CTX = ssl.create_default_context()


def load(name, default):
    p = os.path.join(OUT, name)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else default


def save(name, obj):
    json.dump(obj, open(os.path.join(OUT, name), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
        return json.loads(r.read())


# ───── 1. 좌표 ─────
coords = load("coords.json", {})
used = set()
for days in COURSES.values():
    for d in days:
        for it in d["items"]:
            used.update([it["frm"], it["to"]] if it["kind"] == "move" else [it["place"]])
missing = sorted(k for k in used if k not in PLACES)
if missing:
    sys.exit("places 에 없는 키: %s" % ", ".join(missing))
for key in sorted(used):
    p = PLACES[key]
    if p.get("ll"):
        coords[key] = {"lat": p["ll"][0], "lon": p["ll"][1], "src": "manual"}
    elif key not in coords and NET:
        try:
            hits = get_json("https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({"q": p["q"], "format": "json", "limit": 1}))
            if hits:
                coords[key] = {"lat": float(hits[0]["lat"]), "lon": float(hits[0]["lon"]), "src": hits[0]["display_name"][:80]}
                print("geo ok ", key, coords[key]["src"][:60], flush=True)
            else:
                print("geo NONE", key, p["q"], flush=True)
        except Exception as e:
            print("geo ERR", key, e, flush=True)
        time.sleep(1.2)  # Nominatim 정책: 초당 1회 이하
nocoord = sorted(k for k in used if k not in coords)
if nocoord:
    sys.exit("좌표 없음 (places 에 ll 을 적어 주세요): %s" % ", ".join(nocoord))
save("coords.json", coords)


def ll(key):
    return (coords[key]["lat"], coords[key]["lon"])


# ───── 2. 지도 구간 · 도보 경로 ─────
routes = load("routes.json", {})


def foot_route(a, b):
    k = "%s|%s" % (a, b)
    if k in routes or not NET:
        return
    (la1, lo1), (la2, lo2) = ll(a), ll(b)
    url = "https://routing.openstreetmap.de/routed-foot/route/v1/foot/%f,%f;%f,%f?overview=full&geometries=geojson" % (lo1, la1, lo2, la2)
    try:
        data = get_json(url)
        routes[k] = [[round(p[1], 6), round(p[0], 6)] for p in data["routes"][0]["geometry"]["coordinates"]]
    except Exception as e:
        print("route fail", k, e, flush=True)
        routes[k] = [list(ll(a)), list(ll(b))]
    time.sleep(0.6)


index = {}
marker_of = {}  # (course, day, item idx) → {장소키: 번호}
for c, days in COURSES.items():
    for dn, day in enumerate(days, 1):
        segs, cur = [], []
        for idx, it in enumerate(day["items"]):
            if it["kind"] == "move" and it["mode"] in LONG_HAUL:
                if cur:
                    segs.append(cur)
                cur = []
                continue
            cur.append((idx, it))
        if cur:
            segs.append(cur)
        sn = 0
        for seg in segs:
            order = {}
            for idx, it in seg:
                for k in ([it["frm"], it["to"]] if it["kind"] == "move" else [it["place"]]):
                    order.setdefault(k, len(order) + 1)
                if it["kind"] == "move" and it["mode"] == "walk":
                    foot_route(it["frm"], it["to"])
            if len(order) < 2:
                continue
            sn += 1
            name = "c%d_d%02d_s%d.png" % (c, dn, sn)
            index[name] = {"course": c, "day": dn, "seg": sn, "order": order, "items": [i for i, _ in seg], "city": day["city"]}
            for idx, _ in seg:
                marker_of[(c, dn, idx)] = order
save("index.json", index)
save("routes.json", routes)


# ───── 3. 날짜 사진 (커먼즈) ─────
cred_path = os.path.join(PHOTO_DIR, "credits.json")
credits = json.load(open(cred_path, encoding="utf-8")) if os.path.exists(cred_path) else {}
for key, (alt, queries) in trip.PHOTOS.items():
    fn = os.path.join(PHOTO_DIR, key + ".jpg")
    if key in credits and os.path.exists(fn):
        continue
    if not NET:
        continue
    pick = commons.first(queries)
    if not pick:
        print("photo NONE", key)
        continue
    open(fn, "wb").write(commons.fetch(pick["thumb"]))
    credits[key] = dict(pick, alt=alt)
    print("photo ok", key, pick["title"][:60], pick["license"], flush=True)
    json.dump(credits, open(cred_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    time.sleep(1)


# ───── 4. courses.json ─────
def dir_url(frm, to, mode):
    return "https://www.google.com/maps/dir/?api=1&origin=%.5f,%.5f&destination=%.5f,%.5f&travelmode=%s" % (
        ll(frm) + ll(to) + (GMAP_MODE.get(mode, "transit"),))


def place_url(key):
    return "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(PLACES[key]["q"])


def build_item(it, order):
    def num(key):
        return "%d " % order[key] if key in order else ""
    if it["kind"] == "move":
        head = "%s%s → %s%s" % (num(it["frm"]), PLACES[it["frm"]]["ko"], num(it["to"]), PLACES[it["to"]]["ko"])
        return {"time": it["time"], "kind": "move", "mode": it["mode"], "head": head,
                "line": " · ".join(p for p in (it.get("line"), it.get("stops")) if p), "note": it.get("note", ""),
                "dur": "%s %d분" % (MODE_KO.get(it["mode"], "이동"), it["mins"]), "fare": it.get("fare", ""), "eur": eur_of(it.get("fare")),
                "mapUrl": dir_url(it["frm"], it["to"], it["mode"]), "mapLabel": "경로 지도 ↗", "link": ""}
    wait = "대기 %d분 → " % it["wait"] if it.get("wait") else ""
    return {"time": it["time"], "kind": "stop", "mode": "", "head": "%s%s" % (num(it["place"]), PLACES[it["place"]]["ko"]),
            "line": it["do"], "note": it.get("note", ""), "dur": "%s%d분" % (wait, it["dur"]),
            "fare": it.get("fare", ""), "eur": eur_of(it.get("fare")),
            "mapUrl": place_url(it["place"]), "mapLabel": "위치 ↗", "link": it.get("link", "")}


web = {}
for c, days in COURSES.items():
    name, accent = trip.COURSE_META[c]
    out_days, prev = [], None
    for dn, day in enumerate(days, 1):
        items = [build_item(it, marker_of.get((c, dn, i), {})) for i, it in enumerate(day["items"])]
        d = {"n": dn, "date": day["date"], "dow": day["dow"], "city": day["city"], "title": day["title"],
             "note": day.get("note", ""), "start": day["start"], "end": day["end"], "items": items, "maps": [],
             "cost": round(sum(i["eur"] for i in items), 2)}
        pc = credits.get(day.get("photo"))
        if pc:
            d["photo"] = {"alt": pc["alt"], "credit": "사진: %s · %s · %s" % (pc["alt"], pc["artist"], pc["license"]),
                          "page": pc["page"], "file": "photos/%s/%s.jpg" % (K, day["photo"])}
        if dn == 1:
            d.update(trip.ARRIVAL)
        else:
            hotel = trip.HOTELS[prev][0]
            d.update(wake=shift(day["start"], 75), sleepAt="%s 객실 (어젯밤 숙소)" % hotel,
                     bfA=trip.BREAKFAST.get(prev, "호텔 조식"), bfB=trip.CAFES.get(prev, ""),
                     startNote="짐 챙겨 호텔 로비에서 나가기" if day["sleep"] != prev else "호텔 로비에서 나가기")
        if day.get("sleep"):
            hname, hurl, hprice = trip.HOTELS[day["sleep"]]
            d.update(sleepName=hname, sleepUrl=hurl, sleepPrice="%s (2인 1실)" % hprice)
        else:
            d.update(sleepName="기내 (인천행 비행)", sleepUrl="https://www.skyscanner.co.kr", sleepPrice="항공권에 포함")
        prev = day.get("sleep")
        out_days.append(d)
    web["course%d" % c] = {"name": name, "accent": accent, "days": out_days}
save("courses.json", web)

# 스페인 courses.json 은 day.cost 를 app.js 가 합산한다 — 같은 필드를 채웠다
save("budget.json", trip.BUDGET)


# ───── 5. booking.json (숙소는 잠자리에서 자동) ─────
def q(s):
    return urllib.parse.quote(s)


def hotel_items(c):
    runs = []
    for d in web["course%d" % c]["days"]:
        key = COURSES[c][d["n"] - 1].get("sleep")
        if not key:
            continue
        if runs and runs[-1]["key"] == key and runs[-1]["last"] == d["n"] - 1:
            runs[-1]["nights"] += 1
            runs[-1]["last"] = d["n"]
        else:
            m, dd = d["date"].split("/")
            runs.append({"key": key, "checkin": "2027-%02d-%02d" % (int(m), int(dd)), "nights": 1, "last": d["n"]})
    out = []
    for r in runs:
        name, url, price = trip.HOTELS[r["key"]]
        meta = trip.HOTEL_META[r["key"]]
        co = (date.fromisoformat(r["checkin"]) + timedelta(days=r["nights"])).isoformat()
        s = meta["search"]
        links = [
            {"name": "아고다", "tag": "한국어", "url": "https://www.agoda.com/ko-kr/search?textToSearch=%s&checkIn=%s&los=%d&rooms=1&adults=2&children=0" % (q(s), r["checkin"], r["nights"])},
            {"name": "부킹닷컴", "tag": "한국어", "url": "https://www.booking.com/searchresults.ko.html?ss=%s&checkin=%s&checkout=%s&group_adults=2&no_rooms=1&group_children=0" % (q(s), r["checkin"], co)},
            {"name": "트립닷컴", "tag": "한국어", "url": "https://kr.trip.com/hotels/list?keyword=%s&checkin=%s&checkout=%s&adult=2" % (q(s), r["checkin"].replace("-", "/"), co.replace("-", "/"))},
        ]
        if meta.get("official"):
            links.append({"name": "공식 사이트", "tag": "공식", "url": meta["official"]})
        when = meta.get("when", "2027년 5월 요금이 열리는 대로. 무료 취소 요금으로 먼저 잡기")
        out.append({"what": name, "where": meta["city"],
                    "dates": "%s 체크인 · %d박 (%s 체크아웃)" % (r["checkin"][5:].replace("-", "/"), r["nights"], co[5:].replace("-", "/")),
                    "price": price + " · 1박 2인 1실", "when": when, "alt": meta.get("alt", ""), "links": links})
    return out


bk = {"generated": date.today().isoformat(), "country": trip.BOOKING["country"], "sites": trip.BOOKING["sites"], "taxi": trip.BOOKING["taxi"], "courses": {}}
for c in COURSES:
    groups = []
    for g in trip.BOOKING["courses"][c]["groups"]:
        items = hotel_items(c) if g.get("auto") == "hotels" else g["items"]
        groups.append({"cat": g["cat"], "hint": g["hint"], "items": [dict(it, due=due_of(it["when"])) for it in items]})
    bk["courses"]["course%d" % c] = {"name": trip.BOOKING["courses"][c]["name"], "groups": groups}
save("booking.json", bk)


# ───── 6. restaurants.json (가게 + 대표 음식 사진) ─────
fcred_path = os.path.join(FOOD_DIR, "credits.json")
fcred = json.load(open(fcred_path, encoding="utf-8")) if os.path.exists(fcred_path) else {}
rest = {}
for key, r in trip.RESTAURANTS.items():
    rec = fcred.setdefault(key, {})
    if NET and not (rec.get("shop") and os.path.exists(os.path.join(FOOD_DIR, key + ".jpg"))):
        pick = commons.first(r.get("shop_q", []))
        kind = "shop"
        if not pick and r.get("dish_q"):
            pick, kind = commons.first(r["dish_q"][:1]), "dish"
        if pick:
            open(os.path.join(FOOD_DIR, key + ".jpg"), "wb").write(commons.fetch(pick["thumb"]))
            rec["shop"] = dict(pick, kind=r.get("shop_kind", "shop") if kind == "shop" else kind)
            print("food ok ", key, kind, pick["title"][:50], flush=True)
        time.sleep(1)
    dishes = rec.setdefault("dishes", [])
    used_titles = {rec.get("shop", {}).get("title")} | {d["title"] for d in dishes}
    for i, dq in enumerate(r.get("dish_q", [])[:2], 1):
        fn = "%s_d%d.jpg" % (key, i)
        if any(d["file"] == fn for d in dishes) and os.path.exists(os.path.join(FOOD_DIR, fn)):
            continue
        if not NET:
            continue
        pick = commons.first([dq], exclude=used_titles)
        if pick:
            open(os.path.join(FOOD_DIR, fn), "wb").write(commons.fetch(pick["thumb"]))
            used_titles.add(pick["title"])
            dishes[:] = [d for d in dishes if d["file"] != fn] + [dict(pick, file=fn, dish=dq)]
            print("dish ok ", fn, pick["title"][:50], flush=True)
        time.sleep(1)
    json.dump(fcred, open(fcred_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    shop = rec.get("shop")
    if shop and r.get("shop_kind") and shop.get("kind") == "shop":
        shop["kind"] = r["shop_kind"]
    photo = None
    if shop and os.path.exists(os.path.join(FOOD_DIR, key + ".jpg")):
        photo = {"file": "photos/%s/food/%s.jpg" % (K, key), "kind": shop["kind"],
                 "credit": "%s · %s · Wikimedia Commons" % (shop["artist"], shop["license"]), "page": shop["page"]}
    dl = [{"file": "photos/%s/food/%s" % (K, d["file"]), "dish": d["dish"], "credit": "%s · %s · Wikimedia Commons" % (d["artist"], d["license"]), "page": d["page"]}
          for d in dishes if os.path.exists(os.path.join(FOOD_DIR, d["file"]))]
    rest[key] = {k: v for k, v in r.items() if k not in ("shop_q", "dish_q", "shop_kind")}
    rest[key].update(photo=photo, dishes=dl)
save("restaurants.json", rest)
if not os.path.exists(os.path.join(OUT, "previews.json")):  # 링크 미리보기는 fetch_previews.py 로 따로 (없으면 빈 파일)
    save("previews.json", {})

print("%s: %d courses, %d coords, %d map segs, %d routes, %d photos, %d restaurants" % (
    K, len(web), len(coords), len(index), len(routes), len(credits), len(rest)))
