"""tiles.json 에 적힌 (z,x,y) 타일을 OpenStreetMap 에서 받아 tiles/ 폴더에 저장한다.
사용: python -I fetch_tiles.py <tiles.json> <out_dir>"""
import json, os, sys, time, urllib.request

tiles = json.load(open(sys.argv[1]))
out = sys.argv[2]
os.makedirs(out, exist_ok=True)
UA = "SpainHoneymoonPlanner/1.0 (personal trip planner; contact: hoyoungpark.home@gmail.com)"
done = fail = 0
for z, x, y in tiles:
    p = os.path.join(out, "%d_%d_%d.png" % (z, x, y))
    if os.path.exists(p):
        done += 1
        continue
    url = "https://tile.openstreetmap.org/%d/%d/%d.png" % (z, x, y)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        open(p, "wb").write(data)
        done += 1
    except Exception as e:
        fail += 1
        print("fail", z, x, y, e, flush=True)
    time.sleep(0.15)
    if done % 100 == 0:
        print("progress", done, "/", len(tiles), flush=True)
print("done", done, "fail", fail, flush=True)
