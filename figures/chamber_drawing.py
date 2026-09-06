#!/usr/bin/env python3
"""Technical drawing of the plant sampling chamber (chamber only).

Front section view + top view at 1:5, dimensioned in mm, balloon callouts
with a parts list. Enclosure 400 x 300 x 400 mm (W x D x H) with a 1 L glass
sampling jar inside; two 6 mm gas ports on the jar lid leave through bulkhead
unions on opposite enclosure walls at the same height (outlet left -> ADM,
return right <- pump); cutting rod through both lids; fan and T/RH on the
back wall; LED strip under the lid.

Output: figures/chamber_drawing.{pdf,svg,png}
"""
from pathlib import Path
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon

OUT = Path(__file__).resolve().parent
W, H = 244.0, 146.0          # canvas, mm
S = 1 / 5                    # drawing scale (1:5)

INK = "#111111"
GREY = "#666666"
FILL = "#DDDDDD"
FS = 6.0
FS_S = 5.2
FS_D = 5.6                   # dimension text

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": FS,
                     "pdf.fonttype": 42, "svg.fonttype": "none"})
fig = plt.figure(figsize=(W / 25.4, H / 25.4))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H)
ax.set_aspect("equal"); ax.axis("off")

LW_OBJ, LW_THIN, LW_WALL = 0.8, 0.45, 1.6

# ── drafting helpers ─────────────────────────────────────────────────
def seg(x0, y0, x1, y1, lw=LW_OBJ, c=INK, ls="-", z=3):
    ax.plot([x0, x1], [y0, y1], color=c, lw=lw, ls=ls, solid_capstyle="butt", zorder=z)

def arrow_head(x, y, ang_deg, size=1.4, c=INK):
    a = math.radians(ang_deg)
    p = [(x, y),
         (x - size * math.cos(a - 0.35), y - size * math.sin(a - 0.35)),
         (x - size * math.cos(a + 0.35), y - size * math.sin(a + 0.35))]
    ax.add_patch(Polygon(p, closed=True, fc=c, ec="none", zorder=4))

def dim_h(x0, x1, y, text, ext_from=None, off=1.2, text_x=None):
    """Horizontal dimension x0..x1 at height y; extension lines from ext_from (y)."""
    if ext_from is not None:
        for x in (x0, x1):
            seg(x, ext_from + (off if y > ext_from else -off), x,
                y + (0.8 if y > ext_from else -0.8), lw=LW_THIN)
    seg(x0, y, x1, y, lw=LW_THIN)
    arrow_head(x0, y, 180); arrow_head(x1, y, 0)
    ax.text((x0 + x1) / 2 if text_x is None else text_x, y + 0.9, text,
            ha="center", va="bottom", fontsize=FS_D, color=INK)

def dim_v(y0, y1, x, text, ext_from=None, off=1.2, side="left", ext_start=None):
    """Vertical dimension y0..y1 at x. ext_start overrides where extension lines begin."""
    if ext_from is not None:
        for y in (y0, y1):
            xs = ext_from + (-off if x < ext_from else off) if ext_start is None else ext_start
            seg(xs, y, x + (-0.8 if x < ext_from else 0.8), y, lw=LW_THIN)
    seg(x, y0, x, y1, lw=LW_THIN)
    arrow_head(x, y0, 270); arrow_head(x, y1, 90)
    tx = x - 0.9 if side == "left" else x + 0.9
    ax.text(tx, (y0 + y1) / 2, text, ha="right" if side == "left" else "left",
            va="center", fontsize=FS_D, color=INK, rotation=90)

def balloon(n, x, y, tx, ty):
    """Callout balloon at (x, y) with leader to (tx, ty)."""
    seg(x, y, tx, ty, lw=LW_THIN, c=INK, z=5)
    ax.add_patch(Circle((tx, ty), 0.45, fc=INK, ec="none", zorder=6))
    ax.add_patch(Circle((x, y), 2.3, fc="white", ec=INK, lw=0.7, zorder=6))
    ax.text(x, y, str(n), ha="center", va="center", fontsize=FS_S, color=INK, zorder=7,
            fontweight="bold")

def centerline(x0, y0, x1, y1):
    seg(x0, y0, x1, y1, lw=0.4, c=GREY, ls=(0, (6, 1.5, 1, 1.5)), z=1)

def hatch_wall(x, y, w, h):
    ax.add_patch(Rectangle((x, y), w, h, fc="none", ec=INK, lw=LW_WALL, zorder=3,
                           hatch="/////"))

def union(cx, cy):
    ax.add_patch(Rectangle((cx - 1.6, cy - 1.3), 3.2, 2.6, fc="white", ec=INK, lw=0.6, zorder=4))

# ── FRONT SECTION VIEW  (400 x 400 mm -> 80 x 80) ────────────────────
FX0, FY0, FW, FH = 34.0, 46.0, 80.0, 80.0
FX1, FY1 = FX0 + FW, FY0 + FH
CX = FX0 + FW / 2                              # jar / rod axis
T = 0.8                                        # wall thickness on paper (~4 mm)

ax.text(FX0, FY1 + 12.5, "FRONT VIEW · SECTION A–A", fontsize=FS, fontweight="bold", color=INK)

# sectioned walls: floor, left, right; lid + gasket
hatch_wall(FX0 - T, FY0 - T, FW + 2 * T, T)
hatch_wall(FX0 - T, FY0, T, FH)
hatch_wall(FX1, FY0, T, FH)
ax.add_patch(Rectangle((FX0 - T - 1.2, FY1 + 0.9), FW + 2 * T + 2.4, T,
                       fc="none", ec=INK, lw=LW_WALL, zorder=3, hatch="/////"))
ax.add_patch(Rectangle((FX0 - T, FY1), FW + 2 * T, 0.9, fc=FILL, ec=INK, lw=0.4, zorder=3))
ax.text(FX1 + T + 2.0, FY1 + 0.9, "gasket", fontsize=FS_S, color=GREY, va="center", ha="left")

# sampling jar Ø100 x 150 -> 20 x 30, centred on CX
JX0, JX1, JY0, JY1 = CX - 10, CX + 10, FY0, FY0 + 30.0
seg(JX0, JY0, JX0, JY1); seg(JX1, JY0, JX1, JY1)
ax.add_patch(Rectangle((JX0 - 0.8, JY1), (JX1 - JX0) + 1.6, 1.6, fc=FILL, ec=INK, lw=LW_OBJ, zorder=3))
# pot + grass
ax.add_patch(Rectangle((CX - 5, JY0), 10, 4, fc="none", ec=INK, lw=0.5))
for x0, dx in ((CX - 3.5, -1.2), (CX - 1.5, -0.4), (CX + 0.5, 0.4), (CX + 2.5, 1.2)):
    ys = [JY0 + 4 + 12 * t for t in (0, 0.25, 0.5, 0.75, 1.0)]
    xs = [x0 + dx * (2.4 * t) ** 1.6 for t in (0, 0.25, 0.5, 0.75, 1.0)]
    ax.plot(xs, ys, color=INK, lw=0.6)
# jar-lid ports (outlet left, return right)
PL, PR = CX - 6, CX + 6
for px in (PL, PR):
    ax.add_patch(Rectangle((px - 1.2, JY1 + 1.6), 2.4, 1.8, fc="white", ec=INK, lw=0.6, zorder=4))
# cutting rod through both lids, blade above the grass
seg(CX, FY1 + 7.5, CX, JY0 + 18, lw=1.3)
seg(CX - 2.5, JY0 + 18, CX + 2.5, JY0 + 18, lw=1.3)
for gy in (FY1, JY1):                          # grommets
    ax.add_patch(Rectangle((CX - 1.4, gy - 0.3), 2.8, 2.6, fc="white", ec=INK, lw=0.6, zorder=4))
    ax.add_patch(Rectangle((CX - 1.4, gy - 0.3), 2.8, 2.6, fc="none", ec=INK, lw=0.4, zorder=4, hatch="xxxx"))

# gas lines, both ports at 250 mm -> y = FY0 + 50
PY = FY0 + 50.0
seg(PL, JY1 + 3.4, PL, PY); seg(PL, PY, FX0 - T, PY)
seg(PR, JY1 + 3.4, PR, PY); seg(PR, PY, FX1 + T, PY)
union(FX0 - T / 2, PY); union(FX1 + T / 2, PY)
arrow_head(PL, PY - 6, 90); arrow_head(PR, PY - 6, 270)
# external stubs
seg(FX0 - T - 1.6, PY, FX0 - T - 5.5, PY); arrow_head(FX0 - T - 5.5, PY, 180)
ax.text(FX0 - T - 5.2, PY - 1.4, "to ADM", ha="center", va="top", fontsize=FS_S, color=GREY)
seg(FX1 + T + 1.6, PY, FX1 + T + 7, PY); arrow_head(FX1 + T + 1.6, PY, 180)
ax.text(FX1 + T + 5.5, PY - 1.4, "from pump", ha="center", va="top", fontsize=FS_S, color=GREY)

# fan on the back wall (face-on)
fcx, fcy = FX0 + 12.0, FY1 - 12.0
ax.add_patch(Rectangle((fcx - 4.5, fcy - 4.5), 9, 9, fc="none", ec=INK, lw=0.4, zorder=3))
ax.add_patch(Circle((fcx, fcy), 4.0, fc="white", ec=INK, lw=LW_OBJ, zorder=3))
ax.add_patch(Circle((fcx, fcy), 0.6, fc=INK, ec="none", zorder=4))
for a in (0, 60, 120):
    ax.plot([fcx - 4 * math.cos(math.radians(a)), fcx + 4 * math.cos(math.radians(a))],
            [fcy - 4 * math.sin(math.radians(a)), fcy + 4 * math.sin(math.radians(a))],
            color=INK, lw=0.5, zorder=3)
# LED strip under the lid
ax.add_patch(Rectangle((FX0 + 6, FY1 - 2.2), FW - 12, 1.4, fc=FILL, ec=INK, lw=0.4, zorder=3))
# T/RH sensor on the back wall
SX, SY = FX0 + 64, FY1 - 16
ax.add_patch(Rectangle((SX, SY), 8, 5, fc="white", ec=INK, lw=LW_OBJ, zorder=3))
ax.text(SX + 4, SY + 2.5, "T/RH", ha="center", va="center", fontsize=4.6, color=INK, zorder=4)
# cable grommet on the right wall
GY = FY1 - 8
ax.add_patch(Circle((FX1 + T / 2, GY), 1.3, fc="white", ec=INK, lw=0.6, zorder=4))

centerline(CX, FY0 - 4, CX, FY1 + 9)

# dimensions — front view
dim_h(FX0 - T, FX1 + T, 39.5, "400", ext_from=FY0 - T)
dim_v(FY0 - T, FY1 + 0.9 + T, FX0 - T - 16, "400", ext_from=FX0 - T)
dim_v(FY0, PY, FX0 - T - 10, "250", ext_from=FX0 - T, ext_start=FX0 - T - 6.4)
dim_v(JY0, JY1, JX1 + 4.5, "150", ext_from=JX1, side="right")

# ── TOP VIEW  (400 x 300 mm -> 80 x 60), lid removed ─────────────────
TX0, TY0, TW, TH = 142.0, 46.0, 80.0, 60.0
TX1, TY1 = TX0 + TW, TY0 + TH
ax.text(TX0, TY1 + 12.5, "TOP VIEW · lid removed", fontsize=FS, fontweight="bold", color=INK)
ax.add_patch(Rectangle((TX0 - T, TY0 - T), TW + 2 * T, TH + 2 * T, fc="none", ec=INK, lw=LW_WALL, zorder=3))
ax.add_patch(Rectangle((TX0, TY0), TW, TH, fc="none", ec=INK, lw=LW_OBJ, zorder=3))
JCX, JCY, JR = TX0 + TW / 2, TY0 + 30.0, 10.0
ax.add_patch(Circle((JCX, JCY), JR, fc="none", ec=INK, lw=LW_OBJ, zorder=3))
ax.add_patch(Circle((JCX, JCY), JR + 0.8, fc="none", ec=INK, lw=0.4, zorder=3))
centerline(JCX - 14, JCY, JCX + 14, JCY); centerline(JCX, JCY - 14, JCX, JCY + 14)
for px in (JCX - 6, JCX + 6):
    ax.add_patch(Circle((px, JCY), 1.2, fc="white", ec=INK, lw=0.6, zorder=4))
ax.add_patch(Circle((JCX, JCY), 1.0, fc=INK, ec="none", zorder=4))
seg(JCX - 7.2, JCY, TX0 - T, JCY); seg(JCX + 7.2, JCY, TX1 + T, JCY)
union(TX0 - T / 2, JCY); union(TX1 + T / 2, JCY)
seg(TX0 - T - 1.6, JCY, TX0 - T - 4.5, JCY); arrow_head(TX0 - T - 4.5, JCY, 180)
seg(TX1 + T + 1.6, JCY, TX1 + T + 4.5, JCY); arrow_head(TX1 + T + 1.6, JCY, 180)
# fan and T/RH on the back wall (top edge), LED strip hidden under the lid (dashed)
ax.add_patch(Rectangle((TX0 + 7.5, TY1 - 2.2), 9, 2.2, fc="white", ec=INK, lw=0.6, zorder=4))
ax.add_patch(Rectangle((TX0 + 64, TY1 - 2.0), 8, 2.0, fc="white", ec=INK, lw=0.6, zorder=4))
ax.add_patch(Rectangle((TX0 + 6, TY0 + 46), TW - 12, 1.4, fc="none", ec=INK, lw=0.5,
                       ls=(0, (2, 1)), zorder=3))
ax.add_patch(Circle((TX1 + T / 2, TY0 + 50), 1.3, fc="white", ec=INK, lw=0.6, zorder=4))
# section plane A–A: through the jar centre, parallel to the front wall;
# only the ends are drawn, arrows give the viewing direction (towards the back wall)
for sx, d in ((TX0 - 11, 1), (TX1 + 16, -1)):
    seg(sx, JCY, sx + 3.5 * d, JCY, lw=1.1)
    seg(sx, JCY, sx, JCY + 5.5, lw=0.6); arrow_head(sx, JCY + 5.5, 90)
    ax.text(sx, JCY + 6.6, "A", ha="center", va="bottom", fontsize=FS, fontweight="bold")

# dimensions — top view
dim_h(TX0 - T, TX1 + T, 39.5, "400", ext_from=TY0 - T)
dim_v(TY0 - T, TY1 + T, TX1 + 7.5, "300", ext_from=TX1 + T, side="right")
dim_v(TY0, JCY, TX0 - 7.5, "150", ext_from=TX0, ext_start=TX0 - 6.0)
dim_h(JCX - 6, JCX + 6, JCY - 14.5, "60", ext_from=JCY - 1.2, text_x=JCX + 3.5)
seg(JCX + JR * 0.707, JCY - JR * 0.707, JCX + 18, JCY - 16, lw=LW_THIN)
ax.text(JCX + 18.5, JCY - 16.2, "Ø100", ha="left", va="top", fontsize=FS_D, color=INK)

# ── BALLOONS ─────────────────────────────────────────────────────────
balloon(1, FX1 + 12, 122, FX1 + T / 2, 122)
balloon(2, JX0 - 6, 66, JX0, 62)
balloon(3, PL - 8, 80, PL, JY1 + 2.5)
balloon(4, FX0 - T - 5, 108, FX0 - T / 2, PY + 1.3)
balloon(5, PL - 12, 104, PL, PY - 4)
balloon(6, CX - 10, 133, CX, FY1 + 5)
balloon(7, fcx + 10, 121, fcx + 3, fcy + 2.5)
balloon(8, CX + 10, 133, CX + 8, FY1 - 1.5)
balloon(9, SX + 8, 103, SX + 4, SY)
balloon(10, FX1 + 12, 111, FX1 + T / 2, GY + 1.3)

# ── PARTS LIST ───────────────────────────────────────────────────────
parts = [
    (1, "Enclosure", "PP/PE box 400 × 300 × 400, lid + silicone gasket"),
    (2, "Sampling chamber", "borosilicate jar, 1 L (Ø100 × 150), PTFE-faced lid"),
    (3, "Lid port union ×2", "bulkhead, 6 mm tube, PTFE or SS"),
    (4, "Wall bulkhead union ×2", "6 mm tube, PTFE or SS, opposite walls"),
    (5, "Tubing", "PTFE 6 mm OD / 4 mm ID, kept ≥ chamber temperature"),
    (6, "Cutting rod", "SS Ø3 + blade, PTFE grommets in both lids"),
    (7, "Fan", "40 mm brushless DC 12 V, back wall"),
    (8, "LED strip", "white, dimmable, lid underside"),
    (9, "T / RH sensor", "SHT31 or equivalent, logged"),
    (10, "Cable grommet", "silicone, right wall"),
]
PX0, PY0, ROW = FX0 - T - 16, 30.0, 3.9
PX1 = TX1 + 16
ax.text(PX0, PY0 + 1.2, "PARTS LIST", fontsize=FS, fontweight="bold", color=INK)
seg(PX0, PY0 - 0.6, PX1, PY0 - 0.6, lw=0.5)
for i, (n, name, spec) in enumerate(parts):
    col = i // 5
    x = PX0 + col * ((PX1 - PX0) / 2 + 2)
    y = PY0 - 2.4 - (i % 5) * ROW
    ax.text(x, y, f"{n:>2}", ha="left", va="top", fontsize=FS_S, color=INK, fontweight="bold")
    ax.text(x + 5, y, name, ha="left", va="top", fontsize=FS_S, color=INK)
    ax.text(x + 33, y, spec, ha="left", va="top", fontsize=4.8, color=GREY)
seg(PX0, PY0 - 2.4 - 5 * ROW + 0.6, PX1, PY0 - 2.4 - 5 * ROW + 0.6, lw=0.5)

# title strip
ax.text(PX1, 142, "Plant VOC sampling chamber", ha="right", va="top", fontsize=FS + 0.6,
        fontweight="bold", color=INK)
ax.text(PX1, 138.4, "scale 1:5 · dimensions in mm · closed loop at ~1 atm", ha="right", va="top",
        fontsize=FS_S, color=GREY)

for ext in ("pdf", "svg", "png"):
    fig.savefig(OUT / f"chamber_drawing.{ext}", dpi=300 if ext == "png" else None, facecolor="white")
print("wrote chamber_drawing.{pdf,svg,png}")
