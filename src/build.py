"""Build shmeeats index.html from src/template.html.

Inlines: the cat logo (PNG data URI), pre-projected US state outlines
(from us-atlas states-10m, already in d3.geoAlbersUsa 975x610 space),
and a compact US city list (GeoNames cities15000, US rows).

Usage: python3 -I build.py <states-10m.json> <cities15000.txt> <logo.png> <out.html>
"""
import sys, json, base64, pathlib

here = pathlib.Path(__file__).resolve().parent
states_path, cities_path, logo_path, out_path = sys.argv[1:5]

# --- states: decode topojson arcs into SVG path strings -----------------
topo = json.load(open(states_path))
tr = topo.get("transform")
arcs = []
for arc in topo["arcs"]:
    x = y = 0
    pts = []
    for dx, dy in arc:
        x += dx; y += dy
        if tr:
            pts.append((x * tr["scale"][0] + tr["translate"][0], y * tr["scale"][1] + tr["translate"][1]))
        else:
            pts.append((x, y))
    arcs.append(pts)

def ring(arc_ids):
    out = []
    for a in arc_ids:
        pts = arcs[a] if a >= 0 else list(reversed(arcs[~a]))
        if out and out[-1] == pts[0]:
            pts = pts[1:]
        out.extend(pts)
    return out

def fmt(v): 
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s

def path_of(geom):
    rings = []
    if geom["type"] == "Polygon":
        rings = geom["arcs"]
    elif geom["type"] == "MultiPolygon":
        rings = [r for poly in geom["arcs"] for r in poly]
    d = []
    for r in rings:
        pts = ring(r)
        if len(pts) < 3: continue
        d.append("M" + " ".join(f"{fmt(px)},{fmt(py)}" for px, py in pts) + "Z")
    return "".join(d)

states = []
for g in topo["objects"]["states"]["geometries"]:
    states.append({"n": g.get("properties", {}).get("name", ""), "d": path_of(g)})

# --- cities -------------------------------------------------------------
cities = []
for line in open(cities_path, encoding="utf-8"):
    f = line.rstrip("\n").split("\t")
    if len(f) < 15 or f[8] != "US": continue
    name, lat, lon, state, pop = f[1], float(f[4]), float(f[5]), f[10], int(f[14] or 0)
    if not state: continue
    cities.append((pop, name, state, round(lat, 3), round(lon, 3)))
cities.sort(reverse=True)
city_list = [[n, s, la, lo] for _, n, s, la, lo in cities]

# --- logo ---------------------------------------------------------------
logo_uri = "data:image/png;base64," + base64.b64encode(open(logo_path, "rb").read()).decode()

def safe_json(obj):
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")

tpl = open(here / "template.html", encoding="utf-8").read()
import time, hashlib
build_id = time.strftime("%Y%m%d-%H%M%S")
html = (tpl.replace("__BUILD__", build_id).replace("__LOGO__", logo_uri)
           .replace("__STATES__", safe_json(states))
           .replace("__CITIES__", safe_json(city_list)))
open(out_path, "w", encoding="utf-8").write(html)
open(pathlib.Path(out_path).parent / "data" / "build.txt", "w").write(build_id + "\n")
print(f"states={len(states)} cities={len(city_list)} bytes={len(html.encode())}")
