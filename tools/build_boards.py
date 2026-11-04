"""일정 데이터(itinerary.py) + 지도 blob → 코스별 '문앞-문앞' 아트보드(.dc.html)를 만든다.
1) 날짜별 JSON을 만들고 2) 높이를 재서 8000px 안에 들어가게 묶고 3) 템플릿에 심어 저장한다."""
import json
import os
import re
import sys
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from blobs import HOTEL_LINKS, MAP_BLOBS, PHOTO_BLOBS  # noqa: E402
from itinerary import BREAKFAST, CAFES, COURSES  # noqa: E402
from places import PLACES  # noqa: E402

SCRATCH = os.path.dirname(HERE)
COORDS = json.load(open(os.path.join(SCRATCH, "data", "coords.json")))
INDEX = json.load(open(os.path.join(SCRATCH, "data", "index.json")))
PROJECT = os.path.join(SCRATCH, "artifact", "project")
COURSES_JSON = os.path.join(SCRATCH, "data", "courses.json")  # 웹앱용 (maps/photos 는 파일 경로로)
TEMPLATE = open(os.path.join(HERE, "board_template.dc.html"), encoding="utf-8").read()
MAX_H = 8000

MODE_KO = {"walk": "도보", "metro": "메트로", "train": "열차", "rack": "산악열차", "funicular": "푸니쿨라",
           "bus": "버스", "tram": "트램", "taxi": "택시", "plane": "비행기"}
GMAP_MODE = {"walk": "walking", "taxi": "driving"}
COURSE_META = {
    1: ("코스 1 · 스페인 일주 (경유)", "#1E56A0"),
    2: ("코스 2 · 스페인 일주 (직항 가성비)", "#2F7A57"),
    3: ("코스 3 · 안달루시아 + 세고비아 (직항)", "#B8432A"),
}


def latlon(key):
    c = COORDS[key]
    return "%.5f,%.5f" % (c["lat"], c["lon"])


def dir_url(frm, to, mode):
    return "https://www.google.com/maps/dir/?api=1&origin=%s&destination=%s&travelmode=%s" % (
        latlon(frm), latlon(to), GMAP_MODE.get(mode, "transit"))


def place_url(key):
    return "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(PLACES[key]["q"])


def eur_of(fare):
    """요금 문구에서 유로 합계(하한)를 뽑는다. 하루 비용 합산용."""
    if not fare:
        return 0.0
    text = re.sub(r"€\s?(\d+(?:\.\d+)?)\s?[–~-]\s?€?\d+(?:\.\d+)?", r"€\1", fare)
    return sum(float(v) for v in re.findall(r"€\s?(\d+(?:\.\d+)?)", text))


def shift(hhmm, minutes):
    h, m = map(int, hhmm.split(":"))
    t = max(h * 60 + m - minutes, 5 * 60 + 30)
    return "%02d:%02d" % (t // 60, t % 60)


def seg_maps(course, dnum):
    """이 날의 지도 목록과 '아이템 번호 → 지도 위 번호' 표."""
    maps, marker_of = [], {}
    for key, meta in sorted(INDEX.items()):
        if meta["course"] != course or meta["day"] != dnum:
            continue
        stem = key.replace(".png", "")
        order = meta["order"]
        names = " → ".join("%d %s" % (n, PLACES[k]["ko"]) for k, n in sorted(order.items(), key=lambda kv: kv[1]))
        maps.append({"src": MAP_BLOBS[stem], "alt": "%s 이동 경로 지도" % meta["city"],
                     "caption": "지도 %d · %s" % (meta["seg"], names), "file": "maps/%s.jpg" % stem})
        for idx in meta["items"]:
            marker_of[idx] = order
    return maps, marker_of


def build_item(idx, it, marker_of):
    order = marker_of.get(idx, {})
    def num(key):
        return "%d " % order[key] if key in order else ""
    if it["kind"] == "move":
        mode = MODE_KO.get(it["mode"], "이동")
        head = "%s%s → %s%s" % (num(it["frm"]), PLACES[it["frm"]]["ko"], num(it["to"]), PLACES[it["to"]]["ko"])
        line_parts = [p for p in (it.get("line"), it.get("stops")) if p]
        return {"time": it["time"], "kind": "move", "mode": it["mode"], "head": head,
                "line": " · ".join(line_parts), "note": it.get("note", ""),
                "dur": "%s %d분" % (mode, it["mins"]), "fare": it.get("fare", ""), "eur": eur_of(it.get("fare")),
                "mapUrl": dir_url(it["frm"], it["to"], it["mode"]), "mapLabel": "경로 지도 ↗", "link": ""}
    wait = "대기 %d분 → " % it["wait"] if it.get("wait") else ""
    return {"time": it["time"], "kind": "stop", "mode": "", "head": "%s%s" % (num(it["place"]), PLACES[it["place"]]["ko"]),
            "line": it["do"], "note": it.get("note", ""), "dur": "%s%d분" % (wait, it["dur"]),
            "fare": it.get("fare", ""), "eur": eur_of(it.get("fare")),
            "mapUrl": place_url(it["place"]), "mapLabel": "위치 ↗", "link": it.get("link", "")}


def build_day(course, dnum, day, prev_sleep):
    maps, marker_of = seg_maps(course, dnum)
    items = [build_item(i, it, marker_of) for i, it in enumerate(day["items"])]
    photo = PHOTO_BLOBS[day["photo"]]
    out = {"n": dnum, "date": day["date"], "dow": day["dow"], "city": day["city"], "title": day["title"],
           "note": day.get("note", ""), "start": day["start"], "end": day["end"], "items": items, "maps": maps,
           "photo": {"src": photo[0], "alt": photo[1], "credit": "사진: %s · %s" % (photo[1], photo[2]), "page": photo[3],
                     "file": "photos/%s.jpg" % day["photo"]}}
    if dnum == 1:
        out.update(wake="기내", sleepAt="전날 인천 출발, 비행기 안에서 아침", bfA="기내식",
                   bfB="공항 도착층 카페 (커피+빵 약 €5)", startNote="마드리드 공항 도착 시각부터 시작")
    else:
        hotel = HOTEL_LINKS[prev_sleep][0]
        out.update(wake=shift(day["start"], 75), sleepAt="%s 객실 (어젯밤 숙소)" % hotel,
                   bfA=BREAKFAST[prev_sleep],
                   bfB=CAFES[prev_sleep],
                   startNote="짐 챙겨 호텔 로비에서 나가기" if day["sleep"] != prev_sleep else "호텔 로비에서 나가기")
    if day["sleep"]:
        name, url, price = HOTEL_LINKS[day["sleep"]]
        out.update(sleepName=name, sleepUrl=url, sleepPrice="%s (2인 1실, 카약 검색가)" % price)
    else:
        out.update(sleepName="기내 (인천행 야간 비행)", sleepUrl="https://www.skyscanner.co.kr", sleepPrice="항공권에 포함")
    return out


# ───── 높이 측정용: 템플릿을 평범한 HTML로 펼친다 (sc-for / sc-if / {{ }}) ─────
def lookup(ctx, path):
    cur = ctx
    for part in path.split("."):
        cur = cur.get(part, "") if isinstance(cur, dict) else ""
    return cur


def expand(tpl, ctx):
    tag_re = re.compile(r"<sc-(for|if) ([^>]*)>", re.S)
    out, pos = [], 0
    while True:
        m = tag_re.search(tpl, pos)
        if not m:
            out.append(tpl[pos:])
            break
        out.append(tpl[pos:m.start()])
        kind = m.group(1)
        # 짝이 맞는 닫는 태그 찾기 (중첩 고려)
        depth, i = 1, m.end()
        open_re = re.compile(r"<sc-%s[ >]" % kind)
        close = "</sc-%s>" % kind
        while depth:
            n_open = open_re.search(tpl, i)
            n_close = tpl.find(close, i)
            if n_open and n_open.start() < n_close:
                depth += 1; i = n_open.end()
            else:
                depth -= 1; i = n_close + len(close)
        inner = tpl[m.end():i - len(close)]
        attrs = dict(re.findall(r'(\w[\w-]*)="([^"]*)"', m.group(2)))
        if kind == "for":
            lst = lookup(ctx, attrs["list"].strip("{} "))
            for v in lst or []:
                out.append(expand(inner, dict(ctx, **{attrs["as"]: v})))
        else:
            if lookup(ctx, attrs["value"].strip("{} ")):
                out.append(expand(inner, ctx))
        pos = i
    return re.sub(r"\{\{\s*([\w.]+)\s*\}\}", lambda mm: str(lookup(ctx, mm.group(1))), "".join(out))


def render_vals_in_node(dc_html):
    """보드의 renderVals()를 node로 실행해 값을 받아온다 (check_board.js와 같은 방식)."""
    import subprocess
    js = r"""
const fs=require('fs');const html=fs.readFileSync(process.argv[2],'utf8');
const script=html.split('data-dc-script')[1].split('>').slice(1).join('>').split('</script>')[0];
class DCLogic{constructor(){this.props={};}}
const C=new Function('DCLogic',script+'\nreturn Component;')(DCLogic);
process.stdout.write(JSON.stringify(new C().renderVals()));"""
    tmp = os.path.join(SCRATCH, "tools", "_vals.js")
    open(tmp, "w").write(js)
    return json.loads(subprocess.check_output(["node", tmp, dc_html]))


def fill_template(title, badge, accent, height, days):
    return (TEMPLATE.replace("__TITLE__", title).replace("__BADGE__", badge).replace("__ACCENT__", accent)
            .replace("__HEIGHT__", str(height)).replace("__DATA__", json.dumps(days, ensure_ascii=False)))


def measure_days(course, days_json):
    """각 날짜 카드의 실제 렌더 높이(px)를 Playwright로 잰다."""
    from playwright.sync_api import sync_playwright
    name, accent = COURSE_META[course]
    tmp_dc = os.path.join(SCRATCH, "tools", "_measure.dc.html")
    open(tmp_dc, "w", encoding="utf-8").write(fill_template(name, name, accent, 100, days_json))
    vals = render_vals_in_node(tmp_dc)
    body = TEMPLATE.split("<x-dc>")[1].split("</x-dc>")[0].split("</helmet>")[1]
    html = expand(body, vals).replace("height: 100px;", "height: auto;")
    html = html.replace("__TITLE__", name).replace("__BADGE__", name)
    page_html = "<!doctype html><html><head><meta charset='utf-8'><style>body{margin:0}</style></head><body>%s</body></html>" % html
    tmp_html = os.path.join(SCRATCH, "tools", "_measure.html")
    open(tmp_html, "w", encoding="utf-8").write(page_html)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1280, "height": 900})
        pg.goto("file://" + tmp_html)
        pg.wait_for_timeout(500)
        heights = pg.evaluate("Array.from(document.querySelectorAll('body > div > div')).map(e => e.getBoundingClientRect().height)")
        b.close()
    return heights  # [헤더, day1, day2, ...]


def pack(days_json, heights, header_h):
    """카드 높이를 보고 8000px 안에 들어가도록 날짜를 묶는다."""
    groups, cur, cur_h = [], [], 0
    base = 56 * 2 + header_h + 28  # 패딩 + 헤더 + 간격
    for d, h in zip(days_json, heights):
        need = h + 28
        if cur and base + cur_h + need > MAX_H:
            groups.append((cur, base + cur_h))
            cur, cur_h = [], 0
        cur.append(d); cur_h += need
    groups.append((cur, base + cur_h))
    return groups


def main():
    canvas = json.load(open(os.path.join(PROJECT, "canvas.json")))
    keep = ("Main.dc.html", "Transit.dc.html")
    canvas["boards"] = {k: v for k, v in canvas["boards"].items() if k in keep}
    canvas["order"] = [b for b in canvas["order"] if b in keep]
    plan = {}
    x = 0
    web = {}
    for course, days in COURSES.items():
        name, accent = COURSE_META[course]
        prev = None
        days_json = []
        for i, d in enumerate(days):
            days_json.append(build_day(course, i + 1, d, prev))
            prev = d["sleep"]
        web["course%d" % course] = {"name": name, "accent": accent, "days": days_json}
        json.dump(web, open(COURSES_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        if "--json-only" in sys.argv:
            continue
        heights = measure_days(course, days_json)
        print("course", course, "heights", [round(h) for h in heights], flush=True)
        groups = pack(days_json, heights[1:], heights[0])
        y = 2120
        for gi, (group, h) in enumerate(groups):
            height = int(h) + 40
            fname = "C%dP%d.dc.html" % (course, gi + 1)
            badge = "%s · DAY %d–%d" % (name, group[0]["n"], group[-1]["n"])
            title = "%s · %d~%d일차" % (name.split(" · ")[0], group[0]["n"], group[-1]["n"])
            open(os.path.join(PROJECT, fname), "w", encoding="utf-8").write(fill_template(title, badge, accent, height, group))
            canvas["boards"][fname] = {"x": x, "y": y, "w": 1280, "h": height, "title": title}
            canvas["order"].append(fname)
            plan[fname] = (height, [g["n"] for g in group])
            y += height + 120
        x += 1360
    json.dump(canvas, open(os.path.join(PROJECT, "canvas.json"), "w"), ensure_ascii=False)
    for k, v in plan.items():
        print(k, v)


if __name__ == "__main__":
    main()
