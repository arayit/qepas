#!/usr/bin/env python3
"""Does the cis C=C in (Z)-3-hexenyl acetate move the 1235 cm-1 acetate band?

NIST has no gas-phase IR of (Z)-3-hexenyl acetate, so we test the C=C effect on
two pairs that NIST does have (all gas phase, Sadtler-EPA, 4 cm-1 step):

(a) acetates: n-propyl vs allyl acetate. Allyl has the C=C one carbon from the
    ester oxygen, closer than in our target (two CH2 between). n-Hexyl acetate
    (our proxy) is overlaid.
(b) alcohols: 1-hexanol vs (Z)-3-hexen-1-ol. Same six-carbon chain and the same
    cis C=C position as our target; shows which bands the C=C adds.

NIST absorbance scale is arbitrary, so every trace is normalised to its own
maximum inside the plotted window.
Output: figures/cc_bond_effect.{pdf,png}
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "pnnl"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
C_SAT, C_VOC, C_ENE = "#8a8984", "#2a78d6", "#eb6834"
SET_POINT = 1232.46


def load(name, lo, hi):
    d = np.genfromtxt(DATA / name, delimiter=",", comments="#")
    d = d[~np.isnan(d).any(axis=1)]
    d = d[np.argsort(d[:, 0])]
    m = (d[:, 0] >= lo) & (d[:, 0] <= hi)
    x, y = d[m, 0], d[m, 1]
    y = y - y.min()
    return x, y / y.max()


def peak(x, y, lo, hi):
    m = (x >= lo) & (x <= hi)
    return x[m][np.argmax(y[m])]


plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK,
                     "xtick.color": INK2, "ytick.color": INK2})
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.0, 6.4))

# (a) acetates, zoom on the C-O band
lo, hi = 1150, 1350
for f, lab, c, ls in [("propyl_acetate.csv", "n-propyl acetate\n(no C=C)", C_SAT, "-"),
                      ("allyl_acetate.csv", "allyl acetate\n(C=C next to O–CH₂)", C_ENE, "-"),
                      ("hexyl_acetate.csv", "n-hexyl acetate\n(our proxy)", C_VOC, "--")]:
    x, y = load(f, lo, hi)
    p = peak(x, y, 1200, 1280)
    ax1.plot(x, y, color=c, ls=ls, lw=1.6, label=f"{lab}, peak {p:.0f}")
ax1.axvline(SET_POINT, color=INK, lw=0.8, ls=":")
ax1.text(SET_POINT - 2, 1.05, "set point 1232.5", fontsize=8, color=INK, ha="right")
ax1.set_xlim(lo, hi); ax1.set_ylim(0, 1.12)
ax1.set_ylabel("normalised absorbance")
ax1.set_title("(a) Acetate C–O band: a C=C even closer to the ester moves it by 4 cm⁻¹ "
              "(one data point)", fontsize=9, loc="left", color=INK)
ax1.legend(frameon=False, fontsize=8, loc="center right")

# (b) alcohols, full MIRcat window
lo, hi = 1111, 2000
x, y = load("1_hexanol.csv", lo, hi)
ax2.plot(x, y, color=C_SAT, lw=1.6, label="1-hexanol (no C=C)")
x, y = load("z3_hexenol.csv", lo, hi)
ax2.plot(x, y, color=C_ENE, lw=1.6, label="(Z)-3-hexen-1-ol (same C=C as target)")
ax2.axvline(SET_POINT, color=INK, lw=0.8, ls=":")
ax2.annotate("C=C stretch (weak)", xy=(1654, 0.16), xytext=(1640, 0.42), fontsize=8,
             color=INK2, arrowprops=dict(arrowstyle="-", color=INK2, lw=0.7))
for xv, yv in [(1182, 0.43), (1308, 0.53)]:
    ax2.annotate("", xy=(xv, yv + 0.02), xytext=(1235, 0.86),
                 arrowprops=dict(arrowstyle="-", color=INK2, lw=0.7))
ax2.text(1235, 0.88, "chain CH₂ bands shift", fontsize=8, color=INK2, ha="center",
         bbox=dict(fc="white", ec="none", pad=1))
ax2.set_xlim(lo, hi); ax2.set_ylim(0, 1.12)
ax2.set_xlabel("wavenumber (cm⁻¹)"); ax2.set_ylabel("normalised absorbance")
ax2.set_title("(b) What the cis C=C adds: weak extra bands, no strong band of its own",
              fontsize=9, loc="left", color=INK)
ax2.legend(frameon=False, fontsize=8, loc="upper right")

for ax in (ax1, ax2):
    ax.grid(color=GRID, lw=0.6); ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

fig.text(0.01, 0.005, "NIST WebBook gas-phase IR (Sadtler-EPA), 4 cm⁻¹ step; each trace "
         "normalised to its own maximum in the window.", fontsize=7, color=INK2)
fig.tight_layout(rect=(0, 0.02, 1, 1))
out = Path(__file__).with_name("cc_bond_effect")
fig.savefig(out.with_suffix(".pdf")); fig.savefig(out.with_suffix(".png"), dpi=200)
print("wrote", out)
