"""받아 둔 타일 PNG 를 줌 레벨별로 16×16 장짜리 JPEG 아틀라스로 묶는다.
결과: <out>/tiles/atlas_<n>.jpg + <out>/tiles/atlas.json ({"z/x/y": [atlas, col, row]})
사용: python -I build_atlas.py <tiles_dir> <out_dir>"""
import json, os, sys
from PIL import Image

src, out = sys.argv[1], os.path.join(sys.argv[2], "tiles")
os.makedirs(out, exist_ok=True)
N, T = 16, 256
files = sorted(f for f in os.listdir(src) if f.endswith(".png"))
index, atlas_no, sheet, slot = {}, 0, None, 0


def flush():
    global sheet, slot, atlas_no
    if sheet is None:
        return
    rows = (slot + N - 1) // N
    sheet.crop((0, 0, N * T, rows * T)).convert("RGB").save(os.path.join(out, "atlas_%d.jpg" % atlas_no), "JPEG", quality=72, optimize=True)
    atlas_no += 1
    sheet, slot = None, 0


for f in files:
    z, x, y = f[:-4].split("_")
    if sheet is None:
        sheet = Image.new("RGB", (N * T, N * T), (242, 239, 233))
    im = Image.open(os.path.join(src, f)).convert("RGB")
    col, row = slot % N, slot // N
    sheet.paste(im, (col * T, row * T))
    index["%s/%s/%s" % (z, x, y)] = [atlas_no, col, row]
    slot += 1
    if slot == N * N:
        flush()
flush()
json.dump(index, open(os.path.join(out, "atlas.json"), "w"), separators=(",", ":"))
total = sum(os.path.getsize(os.path.join(out, f)) for f in os.listdir(out))
print("tiles", len(index), "atlases", atlas_no, "bytes", total)
