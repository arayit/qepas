#!/usr/bin/env python3
"""NIST gas-phase IR spectrum of methyl salicylate, with our QEPAS set points.

(a) full NIST spectrum, MIRcat window shaded
(b) zoom on 1150-1350 cm-1 with the chosen set points and N2O R15
(c) water absorption in the same window (HITRAN, laser-convolved), log scale

The NIST absorbance scale is arbitrary (no path length or concentration), so
(a) and (b) are normalised to the strongest band. Water in (c) is absolute.

Usage: python3 figures/methyl_salicylate_nist.py [--par path/to/hitran.par]
Output: figures/methyl_salicylate_nist.{pdf,png}
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
C_MESA, C_H2O = "#2a78d6", "#eb6834"
MIRCAT = (1111.0, 2000.0)
SET_POINTS = [(1304.71, "1304.7\nmain"), (1250.28, "1250.3\ncheck"), (1208.74, "1208.7")]
R15 = 1297.8314
ZOOM = (1150.0, 1350.0)
P_H2O = 14.0   # Torr, lab air (exp7 log), same as data/pnnl/FINDINGS.md

ap = argparse.ArgumentParser()
ap.add_argument("--par", default="/home/user/arayit/thesis/data/hitran/h2o_n2o_1111-2000_hitran.par")
args = ap.parse_args()

nu, ab = vbr.load_voc(ROOT / "data/pnnl/methyl_salicylate.csv")
ab = ab - np.percentile(ab, 2)              # remove the flat offset of the NIST trace
norm = ab / ab[(nu >= MIRCAT[0]) & (nu <= MIRCAT[1])].max()

step = 0.002
grid = np.arange(ZOOM[0] - 8, ZOOM[1] + 8, step)
water = vbr.convolve_laser(vbr.water_alpha(grid, vbr.load_water(args.par), P_H2O), step)

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8,
                     "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False})
fig, axes = plt.subplots(3, 1, figsize=(7.0, 7.4), gridspec_kw={"height_ratios": [1, 1.2, 1]})
a, b, c = axes

a.axvspan(*MIRCAT, color=GRID, lw=0)
a.text(np.mean(MIRCAT), 1.04, "MIRcat range", ha="center", va="bottom", color=INK2)
a.plot(nu, norm, color=C_MESA, lw=1.2)
a.set_xlim(nu.max(), nu.min())
a.set_ylim(-0.05, 1.2)
a.set_ylabel("Absorbance (norm.)")
a.set_title("(a) Methyl salicylate, NIST gas-phase IR (4 cm⁻¹ step)", loc="left", color=INK, fontsize=9)

m = (nu >= ZOOM[0]) & (nu <= ZOOM[1])
b.plot(nu[m], norm[m], color=C_MESA, lw=1.4, marker="o", ms=2.5)
for x, lab in SET_POINTS:
    for ax in (b, c):
        ax.axvline(x, color=INK2, lw=0.8, ls="-", zorder=0)
    b.text(x, 1.13, lab, ha="center", va="bottom", color=INK, fontsize=7)
for ax in (b, c):
    ax.axvline(R15, color=INK2, lw=0.8, ls=(0, (3, 2)), zorder=0)
b.text(R15 - 1.0, 0.05, "N₂O R15", ha="left", va="bottom", color=INK2, fontsize=7)
b.set_xlim(ZOOM[1], ZOOM[0])
b.set_ylim(0, 1.32)
b.set_ylabel("Absorbance (norm.)")
b.set_title("(b) Our window, with QEPAS set points", loc="left", color=INK, fontsize=9)

c.semilogy(grid, np.maximum(water, 1e-9), color=C_H2O, lw=0.8)
c.set_xlim(ZOOM[1], ZOOM[0])
c.set_ylim(1e-8, 1e-3)
c.set_ylabel("H₂O absorption (cm⁻¹)")
c.set_xlabel("Wavenumber (cm⁻¹)")
c.set_title(f"(c) Water, HITRAN, {vbr.P_TORR:.0f} Torr total, {P_H2O:.0f} Torr H₂O, laser-convolved",
            loc="left", color=INK, fontsize=9)

for ax in axes:
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
a.set_xlabel("Wavenumber (cm⁻¹)")
fig.text(0.01, 0.005, "NIST scale is arbitrary (no concentration given): positions and shapes only. "
         "Source: NIST WebBook / Sadtler-EPA, CAS 119-36-8.", color=INK2, fontsize=6.5)
fig.tight_layout(rect=(0, 0.02, 1, 1))
out = ROOT / "figures" / "methyl_salicylate_nist"
for ext in ("pdf", "png"):
    fig.savefig(f"{out}.{ext}", dpi=200, facecolor="white")
print(f"wrote {out}.pdf/.png")
