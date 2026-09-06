#!/usr/bin/env python3
"""Experimental-setup schematic for the plant-VOC QEPAS paper.

One figure, three trains that meet at the ADM:
  optical     EC-QCL -> plane mirror -> OAP -> ADM (focus inside resonator)
  gas loop    sampling chamber -> filter -> ADM -> PT tap -> buffer -> pump -> chamber
  electronics function generator (trigger + ref) -> QCL / lock-in -> DAQ

Closed loop at ~1 atm. Sampling chamber (0.5-1 L glass) sits inside a
30 x 40 x 40 cm environmental enclosure with LED lighting, fan and T/RH
logging; the plant is cut from outside through the lid.

Output: figures/setup_schematic.{pdf,svg,png}. Double-column width (180 mm).
Line art only, greyscale-safe, one accent for the laser beam.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Arc, FancyBboxPatch, Polygon

OUT = Path(__file__).resolve().parent
W_MM, H_MM = 180.0, 108.0

INK = "#111111"
GREY = "#6B6B6B"
LIGHT = "#BBBBBB"
BEAM = "#B3261E"          # the one accent: mid-IR beam
FS = 6.4                  # label font size, pt
FS_S = 5.6

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": FS,
    "pdf.fonttype": 42,
    "svg.fonttype": "none",
})

fig = plt.figure(figsize=(W_MM / 25.4, H_MM / 25.4))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W_MM)
ax.set_ylim(0, H_MM)
ax.set_aspect("equal")
ax.axis("off")


# ── helpers ────────────────────────────────────────────────────────────
def box(x, y, w, h, label, sub=None, lw=0.9, fs=FS, r=0.8):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle=f"round,pad=0,rounding_size={r}",
                                fc="white", ec=INK, lw=lw))
    cy = y + h / 2 + (0.9 if sub else 0)
    ax.text(x + w / 2, cy, label, ha="center", va="center", fontsize=fs,
            fontweight="bold" if sub else "normal", color=INK)
    if sub:
        ax.text(x + w / 2, cy - 2.6, sub, ha="center", va="center",
                fontsize=FS_S, color=GREY)


def line(pts, lw=0.9, color=INK, ls="-", arrow=False, arrow_at=None, z=2):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=lw, ls=ls, solid_capstyle="round",
            solid_joinstyle="round", zorder=z)
    if arrow:
        # arrow head on the last segment (or on a chosen segment index)
        i = (arrow_at if arrow_at is not None else len(pts) - 2)
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                    shrinkA=0, shrinkB=0, mutation_scale=7),
                    zorder=z + 1)


def flow_arrow(x, y, dx, dy, color=INK):
    """Small mid-line flow arrow head."""
    ax.annotate("", xy=(x + dx, y + dy), xytext=(x, y),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=0.9,
                                shrinkA=0, shrinkB=0, mutation_scale=6),
                zorder=3)


def label(x, y, s, ha="center", va="center", fs=FS_S, color=GREY, **kw):
    ax.text(x, y, s, ha=ha, va=va, fontsize=fs, color=color, **kw)


def bulkhead(x, y, vertical=True):
    """Two short ticks marking a wall pass-through."""
    if vertical:
        ax.plot([x - 1.2, x + 1.2], [y + 1.6, y + 1.6], color=INK, lw=0.9)
        ax.plot([x - 1.2, x + 1.2], [y - 1.6, y - 1.6], color=INK, lw=0.9)
    else:
        ax.plot([x + 1.6, x + 1.6], [y - 1.2, y + 1.2], color=INK, lw=0.9)
        ax.plot([x - 1.6, x - 1.6], [y - 1.2, y + 1.2], color=INK, lw=0.9)


# ── OPTICAL TRAIN ──────────────────────────────────────────────────────
# QCL
box(4, 82, 36, 12, "EC-QCL", "MIRcat · pulsed · 1111–2000 cm⁻¹")
# beam to plane mirror
line([(40, 88), (69, 88)], color=BEAM, lw=1.1)
flow_arrow(52, 88, 3, 0, color=BEAM)
# plane mirror at (70,88), oriented "\" to send the beam down
ax.plot([67.2, 72.8], [90.8, 85.2], color=INK, lw=2.2, solid_capstyle="butt")
label(74.5, 90.5, "M", ha="left", color=INK, fs=FS)
# beam down to OAP
line([(70, 88), (70, 67)], color=BEAM, lw=1.1)
flow_arrow(70, 78, 0, -3, color=BEAM)
# OAP: concave arc facing the incoming beam, focusing to the right
ax.add_patch(Arc((75.5, 60.5), 13, 13, angle=0, theta1=96, theta2=176,
                 color=INK, lw=2.2))
label(64.5, 60.5, "OAP", ha="right", color=INK, fs=FS)
label(64.5, 57.7, "f = 101.6 mm", ha="right")
# converging beam into the ADM, focus inside resonator, diverging out
fx, fy = 92, 65
ax.add_patch(Polygon([(71.2, 67.4), (71.2, 62.6), (fx, fy)], closed=True,
                     fc=BEAM, ec="none", alpha=0.18, zorder=1))
ax.add_patch(Polygon([(fx, fy), (104, 63.2), (104, 66.8)], closed=True,
                     fc=BEAM, ec="none", alpha=0.18, zorder=1))
line([(71.2, 67.4), (fx, fy), (104, 66.8)], color=BEAM, lw=0.7)
line([(71.2, 62.6), (fx, fy), (104, 63.2)], color=BEAM, lw=0.7)

# ADM (drawn after beam so the box outline sits on top)
ax.add_patch(FancyBboxPatch((80, 58), 24, 14,
                            boxstyle="round,pad=0,rounding_size=0.8",
                            fc="none", ec=INK, lw=1.2, zorder=4))
# resonator tubes + QTF hint inside ADM
ax.add_patch(Rectangle((83.5, 63.6), 6.6, 2.8, fc="white", ec=INK, lw=0.6, zorder=5))
ax.add_patch(Rectangle((93.9, 63.6), 6.6, 2.8, fc="white", ec=INK, lw=0.6, zorder=5))
ax.plot([91.2, 91.2], [61.2, 68.8], color=INK, lw=0.9, zorder=5)
ax.plot([92.8, 92.8], [61.2, 68.8], color=INK, lw=0.9, zorder=5)
ax.text(92, 75, "ADM01", ha="center", va="bottom", fontsize=FS,
        fontweight="bold", color=INK)
label(92, 73.0, "QTF + microresonator", va="bottom")

# ── ELECTRONICS ────────────────────────────────────────────────────────
box(6, 22, 32, 11, "Function generator", "Rigol DG922 · CH1 / CH2")
box(44, 22, 30, 11, "Lock-in amplifier", "EG&G 5110 · 1f AM")
box(44, 5, 30, 9, "DAQ", "10 Hz log", fs=FS)

# trigger FG -> QCL
line([(22, 33), (22, 82)], arrow=True)
label(23.2, 57, "trigger\nf₀ = 12 459 Hz", ha="left", va="center")
# ref FG -> lock-in
line([(38, 27.5), (44, 27.5)], arrow=True)
label(41, 29.6, "ref", fs=FS_S)
# signal ADM -> lock-in
line([(84, 58), (84, 44), (59, 44), (59, 33)], arrow=True)
label(72, 45.6, "QTF signal", va="bottom")
# lock-in -> DAQ
line([(59, 22), (59, 14)], arrow=True)

# ── GAS LOOP ───────────────────────────────────────────────────────────
# enclosure
ax.add_patch(Rectangle((138, 10), 40, 88, fc="none", ec=INK, lw=1.0))
ax.text(148, 100.5, "Environmental enclosure", ha="center", va="bottom",
        fontsize=FS, fontweight="bold", color=INK)
label(148, 98.6, "30 × 40 × 40 cm · T, RH, light logged", va="bottom")
# LED strip at top inside
ax.add_patch(Rectangle((142, 92.5), 22, 2.2, fc=LIGHT, ec=INK, lw=0.5))
label(153, 91.2, "LED", va="top", fs=FS_S)
# fan (top-left inside)
fcx, fcy = 146, 84
ax.add_patch(Circle((fcx, fcy), 3.2, fc="white", ec=INK, lw=0.8))
for a in (0, 60, 120):
    import math
    dx, dy = 3.2 * math.cos(math.radians(a)), 3.2 * math.sin(math.radians(a))
    ax.plot([fcx - dx, fcx + dx], [fcy - dy, fcy + dy], color=INK, lw=0.7)
label(146, 79.4, "fan", va="top")
# T/RH sensor (top-right inside)
ax.add_patch(Rectangle((140.5, 70), 9.5, 5, fc="white", ec=INK, lw=0.8))
label(145.25, 72.5, "T / RH", color=INK, fs=FS_S)
# sampling chamber (glass jar) inside
ax.add_patch(FancyBboxPatch((146, 20), 26, 46,
                            boxstyle="round,pad=0,rounding_size=1.6",
                            fc="white", ec=INK, lw=1.0))
ax.text(156, 61.5, "Sampling chamber", ha="center", va="center",
        fontsize=FS_S, fontweight="bold", color=INK)
label(156, 58.9, "glass · 0.5–1 L", va="center")
# plant: pot + blades
ax.add_patch(Rectangle((153, 21), 12, 5, fc="white", ec=INK, lw=0.7))
for x0, dx in ((155, -1.2), (157, -0.3), (159, 0.4), (161, 0.9), (163, 1.6)):
    ax.plot([x0, x0 + dx, x0 + 2 * dx], [26, 34, 42], color=INK, lw=0.8)
# cutting rod through both lids
ax.plot([168, 168], [106, 40], color=INK, lw=1.6)
ax.plot([161.5, 170], [40, 40], color=INK, lw=1.6)
ax.add_patch(Rectangle((166.8, 96.8), 2.4, 2.4, fc=INK, ec="none", alpha=0.45))
ax.add_patch(Rectangle((166.8, 64.8), 2.4, 2.4, fc=INK, ec="none", alpha=0.45))
label(166, 106.2, "cutting rod, operated from outside", ha="right", va="center")

# loop lines  --------------------------------------------------------
# chamber outlet (146,50) -> filter -> ADM inlet (right face, y=68)
line([(146, 50), (126, 50)])
bulkhead(138, 50, vertical=False)
box(112, 45.5, 14, 9, "Filter", "0.45 µm PTFE", fs=FS_S, r=0.6)
line([(112, 50), (108, 50), (108, 68), (104, 68)], arrow=True)
flow_arrow(136, 50, -3, 0)
# ADM outlet (bottom, x=92) -> down -> PT tap -> buffer -> pump -> chamber
line([(92, 58), (92, 24), (106, 24)])
flow_arrow(92, 40, 0, -3)
# PT dead-end tap off the outlet line
line([(92, 36), (100, 36)])
ax.add_patch(Circle((103.6, 36), 3.4, fc="white", ec=INK, lw=0.9, zorder=4))
ax.text(103.6, 36, "PT", ha="center", va="center", fontsize=FS_S,
        fontweight="bold", color=INK, zorder=5)
label(108.2, 37.6, "Alicat PCD", ha="left", va="center", fs=FS_S)
label(108.2, 34.9, "dead-end tap, suction side", ha="left", va="center", fs=FS_S)
# buffer
box(106, 19.5, 14, 9, "Buffer", "100 mL", fs=FS_S, r=0.6)
line([(120, 24), (124.2, 24)])
# pump
ax.add_patch(Circle((128, 24), 3.8, fc="white", ec=INK, lw=1.0, zorder=4))
ax.text(128, 24, "P", ha="center", va="center", fontsize=FS,
        fontweight="bold", color=INK, zorder=5)
label(128, 18.6, "diaphragm pump\n100–300 sccm", va="top", fs=FS_S)
# pump -> chamber return (146,28)
line([(131.8, 24), (135, 24), (135, 28), (146, 28)], arrow=True)
bulkhead(139.5, 28, vertical=False)
# loop annotation
label(100, 9.5, "PTFE 6 mm · closed loop · p ≈ 1 atm", ha="center", va="top",
      fs=FS_S)

# ── legend-free key: beam colour ──────────────────────────────────────
line([(28, 72), (36, 72)], color=BEAM, lw=1.1)
label(37.5, 72, "mid-IR beam", ha="left", va="center")
line([(28, 68.5), (36, 68.5)], color=INK, lw=0.9)
label(37.5, 68.5, "gas / signal", ha="left", va="center")

for ext in ("pdf", "svg", "png"):
    fig.savefig(OUT / f"setup_schematic.{ext}", dpi=300 if ext == "png" else None,
                facecolor="white")
print("wrote", [str(OUT / f"setup_schematic.{e}") for e in ("pdf", "svg", "png")])
