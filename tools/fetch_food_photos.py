"""식당·대표 음식 사진을 위키미디어 커먼즈에서 받아 photos/food/<키>.jpg 로 저장하고,
저작자·라이선스를 photos/food_credits.json 에 적는다. 가게 이름으로 못 찾으면 대표 음식 사진으로 대신한다.
사용: python -I tools/fetch_food_photos.py   (이미 받은 키는 건너뛴다)"""
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
OUT = os.path.join(ROOT, "photos", "food")
CREDITS = os.path.join(ROOT, "photos", "food_credits.json")
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, HERE)
from commons import fetch, search  # noqa: E402

# 키: (가게 검색어 후보들, 대표 음식 검색어 후보들)
SUBJECTS = {
    "botin": (["Restaurante Botín Madrid", "Sobrino de Botín"], ["Cochinillo asado"]),
    "labra": (["Casa Labra Madrid"], ["Tajada de bacalao", "Bacalao frito"]),
    "bola": (["Taberna La Bola Madrid", "La Bola taberna"], ["Cocido madrileño"]),
    "san_miguel": (["Mercado de San Miguel Madrid interior"], ["Mercado de San Miguel"]),
    "botero": (["Taberna El Botero Toledo"], ["Carcamusas", "Perdiz estofada"]),
    "campos": (["Bodegas Campos Córdoba"], ["Salmorejo cordobés"]),
    "teresas": (["Las Teresas Sevilla bar"], ["Jamón ibérico de bellota"]),
    "rinconcillo": (["El Rinconcillo Sevilla"], ["Espinacas con garbanzos"]),
    "eslava": (["Eslava Sevilla restaurante"], ["Tapas Sevilla"]),
    "diamantes": ([], ["Pescaíto frito", "Fritura de pescado Andalucía"]),
    "morayma": (["Mirador de Morayma Granada"], ["Alhambra desde el Albaicín noche"]),
    "calpep": ([], ["Gambas a la plancha", "Tapas bar Barcelona"]),
    "catalana": ([], ["Patatas bravas tapa", "Montadito de jamón"]),
    "portes": (["7 Portes Barcelona restaurant", "Set Portes Barcelona"], ["Paella de marisco"]),
    "xampanyet": (["El Xampanyet Barcelona"], ["Anchoas del Cantábrico"]),
    "boqueria": (["Mercat de la Boqueria Barcelona"], ["La Boqueria"]),
    "lucio": (["Casa Lucio Madrid"], ["Huevos rotos", "Huevos estrellados"]),
    "candido": (["Mesón de Cándido Segovia"], ["Cochinillo asado Segovia"]),
    "gallo": (["Venta El Gallo Sacromonte"], ["Zambra Sacromonte flamenco", "Cueva Sacromonte"]),
    "mallorquina": (["La Mallorquina Madrid pastelería"], ["Churros con chocolate"]),
    "comercio": (["Bar El Comercio Sevilla"], ["Churros Sevilla"]),
    "futbol": (["Café Fútbol Granada"], ["Churros con chocolate Granada"]),
    "viader": (["Granja Viader Barcelona"], ["Suizo chocolate nata"]),
}




credits = json.load(open(CREDITS, encoding="utf-8")) if os.path.exists(CREDITS) else {}
for key, (shop_qs, dish_qs) in SUBJECTS.items():
    if key in credits and os.path.exists(os.path.join(OUT, key + ".jpg")) and "--force" not in sys.argv:
        continue
    pick = None
    for kind, qs in (("shop", shop_qs), ("dish", dish_qs)):
        for q in qs:
            try:
                res = search(q)
            except Exception as e:
                print("ERR", key, q, e)
                res = []
            if res:
                pick = dict(res[0], kind=kind, query=q)
                break
        if pick:
            break
    if not pick:
        print("none", key)
        continue
    try:
        data = fetch(pick["thumb"])
        open(os.path.join(OUT, key + ".jpg"), "wb").write(data)
        credits[key] = pick
        print("ok ", key, pick["kind"], pick["title"][:60], pick["license"])
    except Exception as e:
        print("ERR dl", key, e)
    json.dump(credits, open(CREDITS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    time.sleep(1)

# ---------- 대표 음식 사진 (가게당 1~2장, <키>_d1.jpg …) ----------
DISHES = {
    "botin": ["Cochinillo asado", "Sopa de ajo"],
    "labra": ["Tajada de bacalao", "Croquetas de bacalao"],
    "bola": ["Cocido madrileño"],
    "san_miguel": ["Tapas Mercado de San Miguel"],
    "botero": ["Carcamusas"],
    "campos": ["Salmorejo cordobés", "Rabo de toro"],
    "teresas": ["Jamón ibérico de bellota", "Espinacas con garbanzos"],
    "rinconcillo": ["Espinacas con garbanzos", "Bacalao con tomate"],
    "eslava": ["Solomillo al whisky", "Tapas Sevilla"],
    "diamantes": ["Pescaíto frito", "Berenjenas con miel"],
    "morayma": ["Remojón granadino", "Rabo de toro"],
    "calpep": ["Gambas a la plancha", "Tortilla de patatas"],
    "catalana": ["Patatas bravas", "Pincho de tortilla de patatas"],
    "portes": ["Paella de marisco", "Crema catalana"],
    "xampanyet": ["Boquerones en vinagre", "Copa de cava"],
    "boqueria": ["Zumo de frutas La Boqueria", "Jamón ibérico"],
    "lucio": ["Huevos rotos", "Callos a la madrileña"],
    "candido": ["Cochinillo asado Segovia", "Judiones de La Granja"],
    "gallo": ["Zambra Sacromonte", "Flamenco Sacromonte"],
    "mallorquina": ["Napolitana de crema", "Churros con chocolate"],
    "comercio": ["Churros con chocolate"],
    "futbol": ["Churros con chocolate"],
    "viader": ["Suizo chocolate nata", "Mel i mató"],
}
for key, qs in DISHES.items():
    rec = credits.setdefault(key, {})
    dishes = rec.setdefault("dishes", [])
    used = {rec.get("title")} | {d["title"] for d in dishes}
    for i, q in enumerate(qs, 1):
        fn = "%s_d%d.jpg" % (key, i)
        if any(d.get("file") == fn for d in dishes) and os.path.exists(os.path.join(OUT, fn)) and "--force" not in sys.argv:
            continue
        try:
            res = [r for r in search(q) if r["title"] not in used]
        except Exception as e:
            print("ERR", key, q, e); res = []
        if not res:
            print("none", key, q); continue
        pick = res[0]
        try:
            open(os.path.join(OUT, fn), "wb").write(fetch(pick["thumb"]))
        except Exception as e:
            print("ERR dl", key, q, e); continue
        used.add(pick["title"])
        dishes = [d for d in dishes if d.get("file") != fn]
        dishes.append(dict(pick, file=fn, dish=q))
        rec["dishes"] = dishes
        print("ok ", fn, pick["title"][:50], pick["license"])
        json.dump(credits, open(CREDITS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        time.sleep(1)
print("done", len(credits))
