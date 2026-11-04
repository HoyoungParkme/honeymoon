"""코스별·일자별 이동 경로 지도를 Leaflet + OSM 타일로 그려 maps/*.jpg 로 저장한다.
도보 구간은 OSRM(foot) 실제 경로, 대중교통·택시는 점선 직선으로 그린다.
사용: python -I tools/render_maps.py [코스번호 ...]
 - data/coords.json 에 없는 장소는 places.py 의 ll 로 채운다
 - 구간의 장소·행 번호가 이전 index.json 과 같고 maps/<이름>.jpg 가 있으면 다시 그리지 않는다"""
import asyncio
import json
import os
import ssl
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from itinerary import COURSES  # noqa: E402
from places import PLACES  # noqa: E402

ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "data")       # coords / routes / index
MAPS = os.path.join(ROOT, "maps")      # 결과 jpg
os.makedirs(MAPS, exist_ok=True)
COORDS = json.load(open(os.path.join(OUT, "coords.json")))
for _k, _p in PLACES.items():
    if _k not in COORDS and _p.get("ll"):
        COORDS[_k] = {"lat": _p["ll"][0], "lon": _p["ll"][1], "src": "manual"}
json.dump(COORDS, open(os.path.join(OUT, "coords.json"), "w"), ensure_ascii=False, indent=1)
ROUTE_CACHE_PATH = os.path.join(OUT, "routes.json")
ROUTES = json.load(open(ROUTE_CACHE_PATH)) if os.path.exists(ROUTE_CACHE_PATH) else {}
UA = "SpainTripMapBuilder/1.0"
CTX = ssl.create_default_context()
LONG_HAUL = {"train", "plane"}  # 이 수단으로 이동하면 도시가 바뀌니 지도를 나눈다


def ll(key):
    c = COORDS[key]
    return (c["lat"], c["lon"])


def foot_route(a, b):
    """두 지점 사이 도보 경로 좌표 목록 (lat, lon). 실패하면 직선."""
    k = "%s|%s" % (a, b)
    if k in ROUTES:
        return ROUTES[k]
    (la1, lo1), (la2, lo2) = ll(a), ll(b)
    url = "https://routing.openstreetmap.de/routed-foot/route/v1/foot/%f,%f;%f,%f?overview=full&geometries=geojson" % (lo1, la1, lo2, la2)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
            data = json.loads(r.read())
        pts = [[p[1], p[0]] for p in data["routes"][0]["geometry"]["coordinates"]]
    except Exception as e:
        print("route fail", k, e, flush=True)
        pts = [list(ll(a)), list(ll(b))]
    ROUTES[k] = pts
    time.sleep(0.6)
    return pts


def segments(day):
    """하루 일정을 장거리 이동(기차·비행기) 기준으로 지도 단위로 나눈다."""
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
    # 지점이 2개 미만이면 지도 의미가 없다
    out = []
    for seg in segs:
        keys = []
        for _, it in seg:
            for k in ([it["frm"], it["to"]] if it["kind"] == "move" else [it["place"]]):
                if not keys or keys[-1] != k:
                    keys.append(k)
        if len(set(keys)) >= 2:
            out.append(seg)
    return out


def build_layers(seg):
    """지도에 그릴 마커(순번)와 선을 만든다."""
    markers, order, lines = [], {}, []
    def mark(key):
        if key not in order:
            order[key] = len(order) + 1
            markers.append({"n": order[key], "lat": ll(key)[0], "lon": ll(key)[1], "name": PLACES[key]["ko"]})
    for idx, it in seg:
        if it["kind"] == "move":
            mark(it["frm"]); mark(it["to"])
            if it["mode"] == "walk":
                lines.append({"mode": "walk", "pts": foot_route(it["frm"], it["to"])})
            else:
                lines.append({"mode": it["mode"], "pts": [list(ll(it["frm"])), list(ll(it["to"]))]})
        else:
            mark(it["place"])
    return markers, lines, order


HTML = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<style>html,body,#m{margin:0;width:1200px;height:640px;font-family:sans-serif}
.pin{background:#1C2230;color:#fff;border:2px solid #fff;border-radius:50%;width:26px;height:26px;line-height:26px;text-align:center;font-weight:700;font-size:13px;box-shadow:0 1px 4px rgba(0,0,0,.4)}
.lg{position:absolute;right:10px;bottom:10px;z-index:1000;background:rgba(255,255,255,.92);padding:8px 10px;border-radius:8px;font-size:12px;color:#1C2230;line-height:1.6}
.lg span{display:inline-block;width:26px;height:0;border-top:3px solid;vertical-align:middle;margin-right:6px}
</style></head><body><div id="m"></div>
<div class="lg"><div><span style="border-color:#1E56A0"></span>도보 (실제 경로)</div><div><span style="border-color:#B8432A;border-top-style:dashed"></span>메트로·열차</div><div><span style="border-color:#2F7A57;border-top-style:dashed"></span>버스·트램</div><div><span style="border-color:#7A5C99;border-top-style:dashed"></span>택시</div></div>
<script>
const D = __DATA__;
const map = L.map('m', {zoomControl:false, attributionControl:true});
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom:19, attribution:'&copy; OpenStreetMap contributors'}).addTo(map);
const color = {walk:'#1E56A0', metro:'#B8432A', train:'#B8432A', rack:'#B8432A', funicular:'#B8432A', bus:'#2F7A57', tram:'#2F7A57', taxi:'#7A5C99', plane:'#7A5C99'};
const group = L.featureGroup();
D.lines.forEach(l => L.polyline(l.pts, {color: color[l.mode] || '#555', weight: l.mode==='walk'?4:3, dashArray: l.mode==='walk'?null:'8 6', opacity:.9}).addTo(group));
D.markers.forEach(mk => L.marker([mk.lat, mk.lon], {icon: L.divIcon({className:'', html:'<div class="pin">'+mk.n+'</div>', iconSize:[26,26], iconAnchor:[13,13]})}).addTo(group));
group.addTo(map);
map.fitBounds(group.getBounds(), {padding:[50,50], maxZoom:16});
window.__ready = false;
let pending = 0;
map.eachLayer(l => { if (l instanceof L.TileLayer) { l.on('loading', ()=>pending++); l.on('load', ()=>{pending--; if(pending<=0) window.__ready = true;}); } });
setTimeout(()=>{ window.__ready = true; }, 15000);
</script></body></html>"""


async def render_all(jobs):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        ctx = await browser.new_context(viewport={"width": 1200, "height": 640}, user_agent=UA, device_scale_factor=1)
        page = await ctx.new_page()
        for job in jobs:
            html_path = job["png"].replace(".png", ".html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(HTML.replace("__DATA__", json.dumps({"markers": job["markers"], "lines": job["lines"]})))
            await page.goto("file://" + os.path.abspath(html_path))
            await page.wait_for_function("window.__ready === true", timeout=30000)
            await page.wait_for_timeout(1200)
            await page.screenshot(path=job["png"])
            from PIL import Image
            Image.open(job["png"]).convert("RGB").save(job["jpg"], "JPEG", quality=85, optimize=True)
            os.remove(job["png"]); os.remove(html_path)
            print("rendered", job["jpg"], flush=True)
        await browser.close()


def main():
    index_path = os.path.join(OUT, "index.json")
    old = json.load(open(index_path)) if os.path.exists(index_path) else {}
    index, jobs = {}, []
    only = sys.argv[1:]  # 예: 1 2 → 코스 1, 2만 (나머지 코스는 이전 index 유지)
    for course, days in COURSES.items():
        if only and str(course) not in only:
            index.update({k: v for k, v in old.items() if v["course"] == course})
            continue
        for di, day in enumerate(days):
            for si, seg in enumerate(segments(day)):
                markers, lines, order = build_layers(seg)
                stem = "c%d_d%02d_s%d" % (course, di + 1, si + 1)
                key = stem + ".png"
                entry = {"course": course, "day": di + 1, "seg": si + 1, "order": order,
                         "items": [idx for idx, _ in seg], "city": day["city"]}
                index[key] = entry
                jpg = os.path.join(MAPS, stem + ".jpg")
                same = old.get(key, {}).get("order") == order and old.get(key, {}).get("items") == entry["items"]
                if not (same and os.path.exists(jpg)):
                    jobs.append({"png": os.path.join(MAPS, stem + ".png"), "jpg": jpg, "markers": markers, "lines": lines})
    for stale in set(os.listdir(MAPS)) - {k.replace(".png", ".jpg") for k in index}:
        os.remove(os.path.join(MAPS, stale)); print("removed stale", stale)
    json.dump(ROUTES, open(ROUTE_CACHE_PATH, "w"))
    json.dump(index, open(index_path, "w"), ensure_ascii=False, indent=1)
    print(len(jobs), "maps to render:", [os.path.basename(j["jpg"]) for j in jobs], flush=True)
    if jobs:
        asyncio.run(render_all(jobs))


main()
