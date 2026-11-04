"""내려받은 사진들을 한 장에 모아 미리보기(컨택트 시트)를 만든다."""
import glob
import os
import sys

from PIL import Image, ImageDraw

image_dir, out_path = sys.argv[1], sys.argv[2]
paths = sorted(glob.glob(os.path.join(image_dir, "*.png")))
thumb_w, thumb_h, label_h, columns = 320, 200, 22, 4
rows = (len(paths) + columns - 1) // columns
sheet = Image.new("RGB", (columns * thumb_w, rows * (thumb_h + label_h)), "white")
draw = ImageDraw.Draw(sheet)
for i, path in enumerate(paths):
    img = Image.open(path).convert("RGB")
    img.thumbnail((thumb_w, thumb_h))
    x, y = (i % columns) * thumb_w, (i // columns) * (thumb_h + label_h)
    sheet.paste(img, (x, y))
    draw.text((x + 4, y + thumb_h + 4), os.path.basename(path), fill="black")
sheet.save(out_path, quality=80)
print(len(paths), "images")
