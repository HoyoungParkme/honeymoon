"""일정 행의 링크(예매·식당·출처)를 Playwright로 열어 스크린샷과 제목을 저장한다.
결과: previews/<해시>.jpg + data/previews.json ({링크: {file, title, desc, host}})
사용: python -I tools/fetch_previews.py   (이미 받은 링크는 건너뛴다)"""
import hashlib
import json
import os
import sys
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "previews")
META = os.path.join(ROOT, "data", "previews.json")
os.makedirs(OUT, exist_ok=True)
courses = json.load(open(os.path.join(ROOT, "data", "courses.json"), encoding="utf-8"))
meta = json.load(open(META, encoding="utf-8")) if os.path.exists(META) else {}

links = []
for c in courses.values():
    for d in c["days"]:
        for it in d["items"]:
            if it.get("link") and it["link"] not in links:
                links.append(it["link"])
todo = [u for u in links if u not in meta or "--force" in sys.argv]
print(len(links), "links,", len(todo), "to fetch", flush=True)
if not todo:
    sys.exit()

from playwright.sync_api import sync_playwright  # noqa: E402

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 1200, "height": 750}, locale="ko-KR",
                              user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36")
    ctx.set_default_timeout(20000)  # evaluate·screenshot까지 모두 20초 상한 (무한 대기 방지)
    for url in todo:
        key = hashlib.md5(url.encode()).hexdigest()[:12]
        rec = {"file": "previews/%s.jpg" % key, "host": urllib.parse.urlsplit(url).netloc.replace("www.", ""), "title": "", "desc": "", "ok": False}
        page = ctx.new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=25000)
            page.wait_for_timeout(2500)
            # 쿠키 배너는 가리기만 한다 (동의 버튼은 누르지 않는다)
            try:
                page.add_style_tag(content="[id*='cookie'],[class*='cookie'],[id*='consent'],[class*='consent'],[id*='gdpr'],[class*='gdpr']{display:none!important}")
            except Exception:  # 리다이렉트 중이면 배너 숨기기는 건너뛴다
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(1500)
            rec["title"] = (page.evaluate("document.querySelector('meta[property=\"og:title\"]')?.content || document.title") or "").strip()[:120]
            rec["desc"] = (page.evaluate("document.querySelector('meta[property=\"og:description\"],meta[name=\"description\"]')?.content || ''") or "").strip()[:200]
            page.screenshot(path=os.path.join(OUT, key + ".jpg"), type="jpeg", quality=70)
            rec["ok"] = True
            print("ok ", rec["host"], rec["title"][:50], flush=True)
        except Exception as e:  # 막힌 사이트는 제목 없이 기록만 남긴다
            rec["file"] = ""
            print("FAIL", url, str(e).splitlines()[0][:80], flush=True)
        finally:
            page.close()
        meta[url] = rec
        json.dump(meta, open(META, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    browser.close()
print("done", sum(1 for r in meta.values() if r["ok"]), "/", len(meta))
