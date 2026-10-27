#!/usr/bin/env python3
"""NIST gas-phase IR spectrum of a candidate VOC, with our QEPAS set points.

(a) full NIST spectrum, MIRcat window shaded
(b) zoom on 1150-1350 cm-1 with the chosen set points and N2O R15
(c) water background in the same window, in mV, same x-axis as (b)

The NIST absorbance scale is arbitrary (no path length or concentration), so
(a) and (b) are normalised to the strongest band. Water in (c) is the HITRAN
absorption converted to lock-in mV with the R14 responsivity anchor (B_RESP);
tall lines are clipped so the floor under each set point stays readable.

Usage: python3 figures/nist_band_figure.py --compound methyl_salicylate|hexyl_acetate
       [--par path/to/hitran.par]
Output: figures/<compound>_nist.{pdf,png}
"""
import argparse
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import voc_band_ranking as vbr  # noqa: E402  (P_TORR = 205 Torr, laser 0.26 cm-1)

INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
C_VOC, C_H2O = "#2a78d6", "#eb6834"
MIRCAT = (1111.0, 2000.0)
R15 = 1297.8314
ZOOM = (1150.0, 1350.0)
P_H2O = 14.0          # Torr, lab air (exp7 log), same as data/pnnl/FINDINGS.md
NOISE = 0.12          # mV, 1-sigma blank (exp9)
YMAX = 0.5            # mV, clip for panel (c)

COMPOUNDS = {
    "methyl_salicylate": dict(
        csv="methyl_salicylate.csv",
        title="Methyl salicylate, NIST gas-phase IR (4 cm⁻¹ step)",
        set_points=[(1304.71, "1304.7\nmain"), (1250.28, "1250.3\ncheck"), (1208.74, "1208.7")],
        extra=[],
        r15_label=(R15 - 1.0, 0.05, "left"),
        note="NIST WebBook / Sadtler-EPA, CAS 119-36-8.",
    ),
    "hexyl_acetate": dict(
        csv="hexyl_acetate.csv",
        title="n-Hexyl acetate, NIST gas-phase IR — proxy for (Z)-3-hexenyl acetate",
        set_points=[(1232.46, "1232.5\nmain")],
        # (Z)-3-hexenyl acetate itself has no gas-phase IR in NIST; its liquid ATR
        # spectrum (SpectraBase JY3GdO5RDHr, via PubChem CID 5363388) peaks here.
        extra=[(1233.0, "(Z)-3-hexenyl acetate\nliquid ATR peak ≈1233")],
        r15_label=(R15 + 1.0, 1.09, "right"),
        note="NIST WebBook / Sadtler-EPA, CAS 142-92-7. (Z)-3-hexenyl acetate has no gas-phase "
             "IR in NIST; its liquid ATR band (SpectraBase via PubChem) is marked.",
    ),
}

ap = argparse.ArgumentParser()
ap.add_argument("--compound", default="methyl_salicylate", choices=sorted(COMPOUNDS))
ap.add_argument("--par", default="/home/user/arayit/thesis/data/hitran/h2o_n2o_1111-2000_hitran.par")
args = ap.parse_args()
cfg = COMPOUNDS[args.compound]

nu, ab = vbr.load_voc(ROOT / "data/pnnl" / cfg["csv"])
ab = ab - np.percentile(ab, 2)              # remove the flat offset of the NIST trace
norm = ab / ab[(nu >= MIRCAT[0]) & (nu <= MIRCAT[1])].max()

step = 0.002
grid = np.arange(ZOOM[0] - 8, ZOOM[1] + 8, step)
water = vbr.convolve_laser(vbr.water_alpha(grid, vbr.load_water(args.par), P_H2O), step)
w_mv = water * vbr.B_RESP

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8,
                     "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False})
fig = plt.figure(figsize=(7.0, 7.6))
gs = fig.add_gridspec(3, 1, height_ratios=[1, 1.2, 1], hspace=0.55)
a = fig.add_subplot(gs[0])
b = fig.add_subplot(gs[1])
c = fig.add_subplot(gs[2], sharex=b)
axes = [a, b, c]

# (a) full spectrum
a.axvspan(*MIRCAT, color=GRID, lw=0)
a.text(np.mean(MIRCAT), 1.04, "MIRcat range", ha="center", va="bottom", color=INK2)
a.plot(nu, norm, color=C_VOC, lw=1.2)
a.set_xlim(nu.max(), nu.min())
a.set_ylim(-0.05, 1.2)
a.set_ylabel("Absorbance (norm.)")
a.set_xlabel("Wavenumber (cm⁻¹)")
a.set_title("(a) " + cfg["title"], loc="left", color=INK, fontsize=9)

# (b) zoom with set points
m = (nu >= ZOOM[0]) & (nu <= ZOOM[1])
b.plot(nu[m], norm[m], color=C_VOC, lw=1.4, marker="o", ms=2.5)
for x, lab in cfg["set_points"]:
    for ax in (b, c):
        ax.axvline(x, color=INK2, lw=0.8, zorder=0)
    b.text(x, 1.13, lab, ha="center", va="bottom", color=INK, fontsize=7)
for x, lab in cfg["extra"]:
    y = float(np.interp(x, nu[m], norm[m]))          # nu is ascending (load_voc sorts it)
    b.annotate(lab, xy=(x, y + 0.03), xytext=(x - 38, 0.78), ha="center", va="bottom",
               fontsize=7, color=INK,
               arrowprops=dict(arrowstyle="->", color=INK2, lw=0.7))
b.axvline(R15, ymax=0.82, color=INK2, lw=0.8, ls=(0, (3, 2)), zorder=0)
c.axvline(R15, color=INK2, lw=0.8, ls=(0, (3, 2)), zorder=0)
rx, ry, rha = cfg["r15_label"]
b.text(rx, ry, "N₂O R15", ha=rha, va="bottom", color=INK2, fontsize=7)
b.set_xlim(ZOOM[1], ZOOM[0])
b.set_ylim(0, 1.32)
b.set_ylabel("Absorbance (norm.)")
b.set_xlabel("Wavenumber (cm⁻¹)")
b.tick_params(labelbottom=True)
b.set_title("(b) Our window, with QEPAS set points", loc="left", color=INK, fontsize=9)

# (c) water in mV, linear, clipped
c.fill_between(grid, 0, np.minimum(w_mv, YMAX), color=C_H2O, alpha=0.25, lw=0)
c.plot(grid, np.minimum(w_mv, YMAX), color=C_H2O, lw=0.8)
c.axhline(NOISE, color=INK, lw=0.9, ls=(0, (4, 2)))
c.text(1196, NOISE + 0.012, "blank noise 0.12 mV", ha="left", va="bottom", color=INK, fontsize=7,
       bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))
for x, _ in cfg["set_points"]:
    v = float(np.interp(x, grid, w_mv))
    c.annotate(f"{v:.3f} mV", xy=(x, v), xytext=(x, 0.36), ha="center", va="bottom", fontsize=7,
               color=INK, arrowprops=dict(arrowstyle="-", color=INK2, lw=0.6),
               bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"))
c.set_ylim(0, YMAX)
c.set_ylabel("H₂O background (mV)")
c.set_xlabel("Wavenumber (cm⁻¹)")
c.set_title(f"(c) Water background, HITRAN, {vbr.P_TORR:.0f} Torr, {P_H2O:.0f} Torr H₂O (lab air); "
            f"lines above {YMAX} mV clipped", loc="left", color=INK, fontsize=9)

for ax in axes:
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
fig.text(0.01, 0.005, "NIST scale is arbitrary: positions and shapes only. " + cfg["note"]
         + " mV via R14 responsivity anchor, ±30-40 %.", color=INK2, fontsize=6.2, wrap=True)
fig.subplots_adjust(left=0.1, right=0.97, top=0.96, bottom=0.08)
out = ROOT / "figures" / f"{args.compound}_nist"
for ext in ("pdf", "png"):
    fig.savefig(f"{out}.{ext}", dpi=200, facecolor="white")
print(f"wrote {out}.pdf/.png")
