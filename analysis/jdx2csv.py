#!/usr/bin/env python3
"""Convert a JCAMP-DX 4.24 (X++(Y..Y)) IR spectrum to two-column CSV."""
import sys, pathlib

def parse(path):
    hdr, data, in_data = {}, [], False
    for line in open(path, errors="replace"):
        line = line.rstrip("\n")
        if line.startswith("##"):
            k, _, v = line[2:].partition("=")
            k = k.strip().upper()
            if k == "XYDATA":
                in_data = True
            elif k == "END":
                in_data = False
            else:
                hdr[k] = v.strip()
            continue
        if in_data and line.strip():
            data.append(line)
    xf = float(hdr.get("XFACTOR", 1))
    yf = float(hdr.get("YFACTOR", 1))
    dx = float(hdr["DELTAX"])
    xs, ys = [], []
    for row in data:
        p = row.split()
        if len(p) < 2:
            continue
        x0 = float(p[0]) * xf
        for i, tok in enumerate(p[1:]):
            xs.append(x0 + i * dx)
            ys.append(float(tok) * yf)
    return hdr, xs, ys

for src in sys.argv[1:]:
    hdr, xs, ys = parse(src)
    name = hdr.get("TITLE", pathlib.Path(src).stem).strip()
    slug = name.lower().replace(" ", "_").replace("-", "_")
    out = pathlib.Path("/home/user/qepas/data/pnnl") / f"{slug}.csv"
    with open(out, "w") as f:
        f.write(f"# {name}  CAS {hdr.get('CAS REGISTRY NO','?')}\n")
        f.write(f"# source: NIST WebBook / {hdr.get('ORIGIN','?')}\n")
        f.write(f"# STATE={hdr.get('STATE','?')}  YUNITS={hdr.get('YUNITS','?')}\n")
        f.write("# NOT QUANTITATIVE: no path length or concentration given.\n")
        f.write("# Absorbance scale is arbitrary -> positions and shapes only.\n")
        f.write("wavenumber_cm-1,absorbance_arbitrary\n")
        for x, y in zip(xs, ys):
            f.write(f"{x:.1f},{y:.6e}\n")
    n = len(xs)
    print(f"{name:22s} {hdr.get('STATE','?'):>5}  {n:4d} pts  "
          f"{min(xs):.0f}-{max(xs):.0f} cm-1  step {float(hdr['DELTAX']):.0f}  "
          f"maxA {max(ys):.3f}  -> {out.name}")
