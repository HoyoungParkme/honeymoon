"""위키미디어 커먼즈에서 여행지 사진을 검색해 내려받고, 저작자·라이선스 정보를 함께 저장한다."""
import json
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request

OUT_DIR = sys.argv[1]
USER_AGENT = "SpainHoneymoonPlanner/1.0 (personal trip page; hoyoungpark.ds@gmail.com)"
CA_BUNDLE = "/root/.ccr/ca-bundle.crt"
SSL_CONTEXT = ssl.create_default_context(cafile=CA_BUNDLE)

# 저장할 이름 -> 커먼즈 검색어
SUBJECTS = {
    "plaza_mayor": "Plaza Mayor Madrid",
    "palacio_real": "Palacio Real Madrid",
    "toledo": "Toledo panorama Tajo",
    "mezquita": "Mezquita Cordoba interior",
    "giralda": "Giralda Sevilla",
    "plaza_espana": "Plaza de España Sevilla",
    "alhambra_view": "Alhambra Mirador San Nicolas",
    "leones": "Patio de los Leones Alhambra",
    "sagrada": "Sagrada Familia Barcelona facade",
    "park_guell": "Park Güell Barcelona",
    "montserrat": "Montserrat monastery Catalonia",
    "gothic": "Barri Gotic Barcelona street",
    "granvia": "Gran Via Madrid",
    "retiro": "Palacio de Cristal Retiro",
    "segovia_aq": "Acueducto de Segovia",
    "segovia_alc": "Alcazar de Segovia",
}


def fetch(url):
    # 429(요청 과다)가 오면 점점 길게 기다렸다가 다시 시도한다
    for attempt in range(6):
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=30, context=SSL_CONTEXT) as response:
                return response.read()
        except urllib.error.HTTPError as error:
            if error.code != 429:
                raise
            time.sleep(15 * (attempt + 1))
    raise RuntimeError("계속 429")


def strip_html(text):
    return re.sub(r"<[^>]+>", "", text or "").strip()


def search(query):
    params = {
        "action": "query", "format": "json", "generator": "search",
        "gsrnamespace": "6", "gsrsearch": query + " filetype:bitmap", "gsrlimit": "8",
        "prop": "imageinfo", "iiprop": "url|extmetadata", "iiurlwidth": "1200",
    }
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    data = json.loads(fetch(url))
    pages = sorted(data.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
    for page in pages:
        info = page.get("imageinfo", [{}])[0]
        meta = info.get("extmetadata", {})
        license_name = meta.get("LicenseShortName", {}).get("value", "")
        is_free = ("CC" in license_name) or ("Public domain" in license_name) or ("PD" in license_name)
        is_landscape = info.get("thumbwidth", 0) > info.get("thumbheight", 1)
        if is_free and is_landscape and info.get("thumburl"):
            return {
                "title": page["title"],
                "thumb": info["thumburl"],
                "page": info.get("descriptionurl", ""),
                "license": license_name,
                "artist": strip_html(meta.get("Artist", {}).get("value", "")),
            }
    return None


import os
credits_path = f"{OUT_DIR}/credits.json"
results = json.load(open(credits_path, encoding="utf-8")) if os.path.exists(credits_path) else {}
SUBJECTS["giralda"] = "Catedral de Sevilla Giralda"
# 처음 고른 사진이 어울리지 않아서 검색어를 바꾼 것들
SUBJECTS["gothic"] = "Pont del Bisbe Barcelona"
SUBJECTS["granvia"] = "Edificio Metropolis Madrid Gran Via"
SUBJECTS["montserrat"] = "Monasterio de Montserrat"
SUBJECTS["sagrada"] = "Sagrada Familia exterior Barcelona"
for retry_key in sys.argv[2:]:
    results.pop(retry_key, None)
for key, query in SUBJECTS.items():
    if key in results:
        continue  # 이미 받은 사진은 건너뛴다
    try:
        found = search(query)
        if found:
            image_bytes = fetch(found["thumb"])
            with open(f"{OUT_DIR}/{key}.jpg", "wb") as f:
                f.write(image_bytes)
            results[key] = found
            print(key, "OK", found["license"], found["title"], flush=True)
            json.dump(results, open(credits_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        else:
            print(key, "NO MATCH", flush=True)
    except Exception as error:  # 하나가 실패해도 나머지는 계속
        print(key, "ERROR", error, flush=True)
    time.sleep(4)  # 위키미디어 요청 제한을 피하려고 간격을 둔다

with open(f"{OUT_DIR}/credits.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
