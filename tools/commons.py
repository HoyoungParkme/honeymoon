"""위키미디어 커먼즈 사진 검색·내려받기 (라이선스 있는 사진만). fetch_food_photos.py·build_country.py 가 쓴다."""
import json
import re
import ssl
import time
import urllib.parse
import urllib.request

UA = "SpainHoneymoonPlanner/1.0 (personal trip page)"
CTX = ssl.create_default_context()


def fetch(url):
    for attempt in range(5):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(10 * (attempt + 1))
    raise RuntimeError("429 계속")


def _strip(t):
    return re.sub(r"<[^>]+>", "", t or "").strip()


def search(q, width=1200):
    """검색어로 CC/퍼블릭 도메인 사진 후보를 순서대로 돌려준다. "File:이름.jpg" 를 주면 그 파일 하나만."""
    if q.startswith("File:"):
        params = {"action": "query", "format": "json", "titles": q, "prop": "imageinfo",
                  "iiprop": "url|extmetadata", "iiurlwidth": str(width)}
    else:
        params = {"action": "query", "format": "json", "generator": "search", "gsrnamespace": "6",
                  "gsrsearch": q + " filetype:bitmap", "gsrlimit": "8", "prop": "imageinfo",
                  "iiprop": "url|extmetadata", "iiurlwidth": str(width)}
    data = json.loads(fetch("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)))
    out = []
    for p in sorted(data.get("query", {}).get("pages", {}).values(), key=lambda x: x.get("index", 99)):
        ii = (p.get("imageinfo") or [{}])[0]
        meta = ii.get("extmetadata", {})
        lic = _strip(meta.get("LicenseShortName", {}).get("value", ""))
        if not ii.get("thumburl") or not re.search(r"CC|Public domain", lic, re.I):
            continue
        if re.search(r"\.(svg|gif|pdf|tif|tiff|webm|ogv)$", p["title"], re.I):
            continue
        out.append({"title": p["title"], "thumb": ii["thumburl"], "page": ii.get("descriptionurl", ""),
                    "license": lic, "artist": _strip(meta.get("Artist", {}).get("value", ""))[:60] or "미상",
                    "w": ii.get("thumbwidth", 0), "h": ii.get("thumbheight", 0)})
    return out


def first(queries, exclude=(), width=1200, ok=None):
    """검색어 후보를 차례로 시도해 처음 나온 사진(제외 목록 밖, ok(사진)이 참인 것)을 고른다."""
    for q in queries:
        try:
            res = [r for r in search(q, width) if r["title"] not in exclude and (ok is None or q.startswith("File:") or ok(r))]
        except Exception as e:  # 네트워크 오류는 다음 검색어로
            print("commons ERR", q, e)
            res = []
        if res:
            return dict(res[0], query=q)
    return None
