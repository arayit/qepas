#!/usr/bin/env python3
"""
OAP Mirror Beam Focusing — QEPAS simulation

Simulation chain
────────────────
  Begin + GaussBeam + Forvard   →  source → OAP  (large grid, Fresnel)
  numpy mask                    →  aperture clip
  np.fft.fft2                   →  OAP focusing  (FFT / Fraunhofer)
  F.field injection + Forvard   →  post-focus propagation (fine grid)

Why FFT instead of Lens()+Forvard():
  At the aperture edge the lens phase varies ~52 000 rad/pixel — far
  beyond Nyquist.  The Fourier method gives the focal-plane field as
  the exact scaled DFT of the aperture field with no phase aliasing.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
from matplotlib.gridspec import GridSpec
from LightPipes import Begin, GaussBeam, Forvard, Intensity, Phase

# ══════════════════════════════════════════════════════════════════
# MIRROR SETTINGS  — change these freely for a different OAP mirror
# ══════════════════════════════════════════════════════════════════
RFL             = 25.4e-3   # Reflected focal length [m]
parent_fl       = 50.8e-3    # Parent parabola FL [m]   (schematic only)
oap_dia         = 25.4e-3    # Physical mirror diameter [m]

# ══════════════════════════════════════════════════════════════════
# BEAM SETTINGS  — change for a different laser / input beam
# ══════════════════════════════════════════════════════════════════
wavelength      = 7.6e-6     # [m]
w0              = 2.5e-3       # Input 1/e² beam waist [m]
z_source_to_oap = 200e-3     # Source-to-OAP distance [m]

# ══════════════════════════════════════════════════════════════════
# FIXED ADM GEOMETRY  — Acoustic Detection Module
#   Physical dimensions of the microresonator.  Do NOT change.
# ══════════════════════════════════════════════════════════════════
tube_r_um      = 800    # µm  inner radius  (Ø 1.6 mm)
tube_len_mm    = 12.4   # mm  tube length
tube_gap_L_mm  = 0.1    # mm  left tube: gap from focus
tube_gap_R_mm  = 0.3    # mm  right tube: gap from focus
z_caus_half_mm = 25.0   # mm  half-length of the caustic window  (±25 mm)

# ─────────────────────────────────────────────────────────────────
# DERIVED QUANTITIES  (computed automatically — do not edit below)
# ─────────────────────────────────────────────────────────────────
clear_ap_r = 0.90 * oap_dia / 2        # clear aperture radius [m]
N          = 512                        # grid pixels per side

# Adaptive input-grid size
#   grid_in must be large enough that the beam at ±z_caus_half fits in
#   the focus grid (focus FOV = N·λ·RFL / grid_in).
#   w(z_edge) ≈ z_caus_half · w0 / RFL  (large-z Gaussian approximation)
z_caus_half = z_caus_half_mm * 1e-3    # [m]
w_at_edge   = z_caus_half * w0 / RFL   # approximate beam size at caustic edge
#   Set grid_in so that focus FOV half = 1.4 × w_at_edge
grid_in = N * wavelength * RFL / (2 * 1.4 * w_at_edge)
grid_in = min(grid_in, 200e-3)         # cap at 200 mm

# Focus grid (derived from Fourier scaling: dx_focus = λ·RFL / grid_in)
dx_focus   = wavelength * RFL / grid_in
grid_focus = N * dx_focus

# Rayleigh range of the input beam and theoretical focus spot
z_R_in          = np.pi * w0**2 / wavelength
w_at_oap        = w0 * np.sqrt(1 + (z_source_to_oap / z_R_in)**2)
w_focus_theory  = wavelength * RFL / (np.pi * w_at_oap)
z_R_focus_theory = np.pi * w_focus_theory**2 / wavelength   # pre-sim estimate

# Tube z-ranges in mm (used for matplotlib)
tubes_mm = [(tube_gap_R_mm, tube_gap_R_mm + tube_len_mm),
            (-(tube_gap_L_mm + tube_len_mm), -tube_gap_L_mm)]

# ── Sanity check ─────────────────────────────────────────────────
n_px_spot = w_focus_theory / dx_focus
if n_px_spot < 3:
    print(f"  WARNING: focus spot is {n_px_spot:.1f} px — consider increasing N.")

print("=" * 60)
print(f"  OAP   RFL = {RFL*1e3:.1f} mm  |  Ø = {oap_dia*1e3:.1f} mm")
print(f"  Beam  λ = {wavelength*1e6:.1f} µm  |  w₀ = {w0*1e3:.0f} mm")
print("=" * 60)
print(f"  Input grid   {grid_in*1e3:.1f} mm · {N}×{N} · {grid_in/N*1e6:.0f} µm/px")
print(f"  Focus grid   {grid_focus*1e3:.2f} mm · {N}×{N} · {dx_focus*1e6:.2f} µm/px")
print(f"  w_focus      {w_focus_theory*1e6:.1f} µm  ({n_px_spot:.1f} px)")
print(f"  z_R (est.)   {z_R_focus_theory*1e3:.2f} mm")
print("=" * 60)

# ─────────────────────────────────────────────────────────────────
# SIMULATION
# ─────────────────────────────────────────────────────────────────

# 1. Source beam
F = Begin(grid_in, wavelength, N)
F = GaussBeam(F, w0)
I_source = Intensity(F)

# Coordinate arrays for input grid
dx_in = grid_in / N
xs_in = (np.arange(N) - N / 2) * dx_in
XX_in, YY_in = np.meshgrid(xs_in, xs_in)
R_in = np.sqrt(XX_in**2 + YY_in**2)

# 2. Free-space propagation to OAP
F = Forvard(F, z_source_to_oap)
I_at_oap = Intensity(F)
P_at_oap = Phase(F)

# 3. Aperture clip
circ_mask   = (R_in <= clear_ap_r).astype(float)
E_apertured = F.field.copy() * circ_mask
I_apertured = np.abs(E_apertured)**2
I_apertured /= I_apertured.max()

# 4. OAP focusing via FFT  (Fraunhofer / thin-lens relation)
E_focus_raw = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(E_apertured)))
E_focus     = E_focus_raw / np.abs(E_focus_raw).max()
I_focus     = np.abs(E_focus)**2
P_focus     = np.angle(E_focus)

# Focus-grid coordinate arrays
xs_f       = (np.arange(N) - N / 2) * dx_focus
XX_f, YY_f = np.meshgrid(xs_f, xs_f)
half       = N // 2

def beam_w(I2d):
    """1/e² radius via intensity-weighted second moment."""
    s = I2d.sum()
    return np.sqrt(2 * ((XX_f**2 + YY_f**2) * I2d).sum() / s) if s > 0 else 0.0

w_focus_sim  = beam_w(I_focus)
z_R_focus    = np.pi * w_focus_sim**2 / wavelength
zR_mm        = z_R_focus * 1e3       # mm — used throughout
w0_f_um      = w_focus_sim * 1e6     # µm — used throughout

print(f"\n  w_focus  sim  {w_focus_sim*1e6:.1f} µm")
print(f"  w_focus  th   {w_focus_theory*1e6:.1f} µm")
print(f"  z_R           {zR_mm:.2f} mm\n")

# 5. Inject focus field into fine-grid LightPipes field
F_focus = Begin(grid_focus, wavelength, N)
F_focus.field[:] = E_focus

# 6. Caustic scan ±z_caus_half (fixed ADM window)
n_caus    = 300
z_caus    = np.linspace(-z_caus_half, z_caus_half, n_caus)
z_caus_mm = z_caus * 1e3
w_caus    = []

r_axis      = xs_f[half:]    # positive r, metres
caustic_img = np.zeros((len(r_axis), n_caus))

# 7. Display planes for Fig 3 — multiples of z_R within ±25 mm
z_disp_mm = [float(np.clip(m * zR_mm, -z_caus_half_mm, z_caus_half_mm))
             for m in [-5, -2, -1, 0, 1, 2, 5]]
z_disp_set = set(z_disp_mm)
fields_disp_dict = {}

# Single pass: caustic scan + 2D image + display-plane capture
print(f"  Caustic scan ±{z_caus_half_mm:.0f} mm ...", end="", flush=True)
for iz, z in enumerate(z_caus):
    Ft = Forvard(F_focus, z)
    It = Intensity(Ft)
    w_caus.append(beam_w(It))
    caustic_img[:, iz] = It[half, half:]
print(" done.")

w_caus = np.array(w_caus) * 1e6                                          # µm
w_th   = w0_f_um * np.sqrt(1 + (z_caus / z_R_focus)**2)                 # µm

caustic_norm = caustic_img / (caustic_img.max(axis=0, keepdims=True) + 1e-30)

# Display planes (small extra propagations, only 7 points)
fields_disp = []
for z in z_disp_mm:
    fields_disp.append(Intensity(Forvard(F_focus, z * 1e-3)))

# ─────────────────────────────────────────────────────────────────
# PLOT STYLE
# ─────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": "#0e1117",
    "axes.facecolor":   "#0e1117",
    "axes.edgecolor":   "#555",
    "axes.labelcolor":  "#ccc",
    "xtick.color":      "#888",
    "ytick.color":      "#888",
    "text.color":       "#ddd",
    "grid.color":       "#2a2a2a",
    "font.family":      "monospace",
    "font.size":        10,
})
CI = "inferno"

def add_cb(ax, im):
    cb = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    cb.ax.tick_params(labelsize=7, colors="#888")

def crop(arr, half_m, dx):
    hp = max(1, int(half_m / dx))
    h  = arr.shape[0] // 2
    s  = slice(h - hp, h + hp)
    return arr[s, s], [-half_m*1e3, half_m*1e3, -half_m*1e3, half_m*1e3]

def draw_tubes(ax, y_bottom, y_top, label=True):
    """Draw ADM microresonator tubes as Rectangle patches."""
    lbl = f"ADM tube  Ø 1.6 mm × {tube_len_mm} mm"
    for i, (z0, z1) in enumerate(tubes_mm):
        rect = Rectangle((z0, y_bottom), z1 - z0, y_top - y_bottom,
                         linewidth=1.5, edgecolor="#ef5350",
                         facecolor="#ef5350", alpha=0.12,
                         label=lbl if (i == 0 and label) else None)
        ax.add_patch(rect)

# ═══════════════════════════════════════════════════════════
# FIG 1 — OAP GEOMETRY SCHEMATIC
# ═══════════════════════════════════════════════════════════
fig1, ax = plt.subplots(figsize=(11, 5), facecolor="#0e1117")
ax.set_facecolor("#0e1117"); ax.axis("off")
ax.set_xlim(-20, 280); ax.set_ylim(-130, 110); ax.set_aspect("equal")

bw  = 12
rfl = RFL * 1e3 * 0.85

# Input beam
ax.fill_betweenx([-bw, bw], 0, 170, color="#4fc3f7", alpha=0.10)
ax.plot([0, 170], [ bw,  bw], "#4fc3f7", lw=1, alpha=0.5)
ax.plot([0, 170], [-bw, -bw], "#4fc3f7", lw=1, alpha=0.5)
ax.annotate("", xy=(162, 0), xytext=(5, 0),
            arrowprops=dict(arrowstyle="-|>", color="#4fc3f7", lw=2))

# OAP mirror
th = np.linspace(0.54*np.pi, 0.93*np.pi, 80)
sc = parent_fl * 1e3 * 0.85
ox = 170 + sc * (1 - np.cos(th))
oy =       sc * np.sin(th)
ax.plot(ox, oy, color="#ffd54f", lw=5, solid_capstyle="round", zorder=4)

# Reflected beam
ax.fill_between([168, 172], 0, -rfl, color="#a5d6a7", alpha=0.18)
ax.plot([168, 168], [0, -rfl], "#a5d6a7", lw=1, alpha=0.5)
ax.plot([172, 172], [0, -rfl], "#a5d6a7", lw=1, alpha=0.5)
ax.annotate("", xy=(170, -rfl+4), xytext=(170, -4),
            arrowprops=dict(arrowstyle="-|>", color="#a5d6a7", lw=2))

ax.plot([170], [-rfl], "*", color="#ff7043", markersize=16, zorder=6)

ax.annotate("", xy=(170, 22), xytext=(0, 22),
            arrowprops=dict(arrowstyle="<->", color="#90caf9", lw=1.3))
ax.text(85, 29, f"z₁ = {z_source_to_oap*1e3:.0f} mm",
        ha="center", color="#90caf9", fontsize=9)

ax.annotate("", xy=(195, 0), xytext=(195, -rfl),
            arrowprops=dict(arrowstyle="<->", color="#ce93d8", lw=1.3))
ax.text(206, -rfl/2, f"RFL = {RFL*1e3:.1f} mm",
        ha="left", va="center", color="#ce93d8", fontsize=9)

ax.plot([170, 182], [0, 0], color="#888", lw=1)
ax.plot([170, 170], [0, -12], color="#888", lw=1)
ax.add_patch(mpatches.Rectangle((170, -12), 12, 12,
    fill=False, edgecolor="#888", lw=1))

ax.text(-2, 0, f"Source\nw₀ = {w0*1e3:.0f} mm", ha="right", va="center",
        color="#4fc3f7", fontsize=9)
ax.text(174, 5, "OAP", color="#ffd54f", fontsize=11, fontweight="bold")
ax.text(174, -rfl - 12, f"Focus  w ≈ {w_focus_sim*1e6:.0f} µm",
        color="#ff7043", fontsize=9)

plt.tight_layout()
plt.savefig("fig1_schematic.png", dpi=150, bbox_inches="tight", facecolor="#0e1117")
print("  Saved: fig1_schematic.png")


# ═══════════════════════════════════════════════════════════
# FIG 2 — INTENSITY AT KEY PLANES
# ═══════════════════════════════════════════════════════════
fig2, axes2 = plt.subplots(1, 4, figsize=(16, 4.5), facecolor="#0e1117")
fig2.suptitle(f"Beam Intensity at Key Planes  —  λ = {wavelength*1e6:.1f} µm  |"
              f"  RFL = {RFL*1e3:.1f} mm",
              color="#fff", fontsize=12)

focus_crop_m = 5 * w_focus_sim     # ±5 w_focus around centre for focus panel

Ic, ec   = crop(I_source,    12e-3,          dx_in)
Ia, ea   = crop(I_at_oap,    12e-3,          dx_in)
Iap, eap = crop(I_apertured, 12e-3,          dx_in)
If, ef   = crop(I_focus,     focus_crop_m,   dx_focus)

panels2 = [
    (Ic,  ec,  "Source  (z = 0)"),
    (Ia,  ea,  f"At OAP  (z = {z_source_to_oap*1e3:.0f} mm)"),
    (Iap, eap, "After aperture"),
    (If,  ef,  f"At focus  (+{RFL*1e3:.0f} mm)"),
]
for ax, (I, ext, title) in zip(axes2, panels2):
    ax.set_facecolor("#0e1117")
    im = ax.imshow(I / I.max(), extent=ext, cmap=CI, origin="lower", vmin=0, vmax=1)
    ax.set_title(title, color="#ddd", fontsize=10, pad=4)
    ax.set_xlabel("mm", fontsize=9)
    ax.set_ylabel("mm", fontsize=9)
    add_cb(ax, im)

plt.tight_layout()
plt.savefig("fig2_key_planes.png", dpi=150, bbox_inches="tight", facecolor="#0e1117")
print("  Saved: fig2_key_planes.png")


# ═══════════════════════════════════════════════════════════
# FIG 3 — BEAM AROUND FOCUS (7 PLANES, each ±1 z_R apart)
# ═══════════════════════════════════════════════════════════
fig3, axes3 = plt.subplots(1, 7, figsize=(18, 3.5), facecolor="#0e1117")
fig3.suptitle(f"Beam Cross-Sections Around Focus  —  z values in multiples of "
              f"z_R = {zR_mm:.2f} mm",
              color="#fff", fontsize=11)

for ax, z_mm, Id in zip(axes3, z_disp_mm, fields_disp):
    ax.set_facecolor("#0e1117")
    # window width scales with beam size at that z
    hw = min(grid_focus / 2, max(1.5 * w_focus_sim,
                                  abs(z_mm) * 1e-3 * 0.35 + 1.5 * w_focus_sim))
    Ic, ext = crop(Id, hw, dx_focus)
    im = ax.imshow(Ic / (Ic.max() + 1e-30), extent=ext,
                   cmap=CI, origin="lower", vmin=0, vmax=1)
    w_here = beam_w(Id) * 1e6
    sign   = "+" if z_mm >= 0 else ""
    ax.set_title(f"z = {sign}{z_mm:.2f} mm\nw = {w_here:.0f} µm",
                 color="#ddd", fontsize=9)
    ax.set_xlabel("mm", fontsize=8)
    ax.tick_params(labelsize=7, colors="#888")

plt.tight_layout()
plt.savefig("fig3_focus_panels.png", dpi=150, bbox_inches="tight", facecolor="#0e1117")
print("  Saved: fig3_focus_panels.png")


# ═══════════════════════════════════════════════════════════
# FIG 4 — BEAM CAUSTIC  w(z)  with ADM tubes
# ═══════════════════════════════════════════════════════════
fig4, ax4 = plt.subplots(figsize=(11, 5), facecolor="#0e1117")
ax4.set_facecolor("#0e1117")
ax4.set_title(f"Beam Caustic After OAP  —  RFL = {RFL*1e3:.1f} mm, "
              f"λ = {wavelength*1e6:.1f} µm", color="#fff", fontsize=12)

ax4.fill_between(z_caus_mm,  w_caus, -w_caus, color="#4fc3f7", alpha=0.15)
ax4.plot(z_caus_mm,  w_caus, "#4fc3f7", lw=2, label="Simulated w(z)")
ax4.plot(z_caus_mm, -w_caus, "#4fc3f7", lw=2)
ax4.plot(z_caus_mm,  w_th,  "--", color="#ff7043", lw=1.5, alpha=0.7,
         label="Gaussian theory")
ax4.plot(z_caus_mm, -w_th,  "--", color="#ff7043", lw=1.5, alpha=0.7)

ax4.axvline( zR_mm, color="#ffd54f", lw=1.2, ls="--", alpha=0.8)
ax4.axvline(-zR_mm, color="#ffd54f", lw=1.2, ls="--", alpha=0.8)
ax4.axhline( w0_f_um, color="#a5d6a7", lw=1.0, ls=":", alpha=0.7)
ax4.axhline(-w0_f_um, color="#a5d6a7", lw=1.0, ls=":", alpha=0.7)

draw_tubes(ax4, -tube_r_um, tube_r_um)

ax4.text( zR_mm + 0.3, w_caus.max() * 0.92, f"+z_R = {zR_mm:.1f} mm",
          color="#ffd54f", fontsize=9)
ax4.text(-zR_mm - 0.3, w_caus.max() * 0.92, f"−z_R",
          color="#ffd54f", fontsize=9, ha="right")
ax4.text(z_caus_mm[-1] - 0.5, w0_f_um + 5,
         f"w_focus = {w0_f_um:.0f} µm", color="#a5d6a7", fontsize=9, ha="right")

ax4.set_xlabel("z from focus [mm]", fontsize=11)
ax4.set_ylabel("Beam radius w(z) [µm]", fontsize=11)
ax4.legend(fontsize=9, facecolor="#1a1a2e", labelcolor="#ddd", loc="upper right")
ax4.grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig("fig4_caustic.png", dpi=150, bbox_inches="tight", facecolor="#0e1117")
print("  Saved: fig4_caustic.png")


# ═══════════════════════════════════════════════════════════
# FIG 5 — RADIAL PROFILES  (at ±1 z_R, ±2 z_R, and focus)
# ═══════════════════════════════════════════════════════════
z_profs = [float(np.clip(m * zR_mm, -z_caus_half_mm, z_caus_half_mm))
           for m in [-2, -1, 0, 1, 2]]
clrs_p  = ["#90caf9", "#81d4fa", "#ff7043", "#ffcc80", "#a5d6a7"]
r_um    = xs_f[half:] * 1e6

fig5, ax5 = plt.subplots(figsize=(9, 5), facecolor="#0e1117")
ax5.set_facecolor("#0e1117")
ax5.set_title(f"Radial Intensity Profiles Near Focus  —  RFL = {RFL*1e3:.1f} mm",
              color="#fff", fontsize=12)

for z_p, c in zip(z_profs, clrs_p):
    It  = Intensity(Forvard(F_focus, z_p * 1e-3))
    prf = It[half, half:]
    sign = "+" if z_p >= 0 else ""
    ax5.plot(r_um, prf / prf.max(), color=c, lw=2,
             label=f"z = {sign}{z_p:.2f} mm")

r_th = np.linspace(0, r_um[-1], 600)
ax5.plot(r_th, np.exp(-2 * (r_th / (w_focus_theory*1e6))**2),
         "w--", lw=1.5, alpha=0.5,
         label=f"Theory  w = {w_focus_theory*1e6:.0f} µm")
ax5.axvline(w_focus_theory*1e6, color="#555", lw=1, ls=":")

ax5.set_xlabel("r [µm]", fontsize=11)
ax5.set_ylabel("Normalised intensity", fontsize=11)
ax5.set_xlim(0, 8 * w_focus_sim * 1e6)   # ±8 w_focus
ax5.legend(fontsize=9, facecolor="#1a1a2e", labelcolor="#ddd")
ax5.grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig("fig5_profiles.png", dpi=150, bbox_inches="tight", facecolor="#0e1117")
print("  Saved: fig5_profiles.png")


# ═══════════════════════════════════════════════════════════
# FIG 6 — BEAM SHAPE EVOLUTION  ±25 mm  (2D CAUSTIC)
# ═══════════════════════════════════════════════════════════
# r display limit: just above tube wall or max beam size (whichever is larger)
r_show = float(min(max(tube_r_um * 1.4, w_caus.max() * 1.1),
                   r_axis[-1] * 1e6))
r_mask  = r_axis * 1e6 <= r_show
img_top = caustic_norm[r_mask, :]
img_bot = img_top[::-1, :]

fig6 = plt.figure(figsize=(13, 8), facecolor="#0e1117")
gs6  = GridSpec(2, 1, figure=fig6, height_ratios=[3, 1.2], hspace=0.06)
ax6t = fig6.add_subplot(gs6[0])
ax6b = fig6.add_subplot(gs6[1], sharex=ax6t)

fig6.suptitle(
    f"Beam Shape Evolution  ±{z_caus_half_mm:.0f} mm Around Focus  —  "
    f"λ = {wavelength*1e6:.1f} µm,  RFL = {RFL*1e3:.1f} mm",
    color="#fff", fontsize=12, y=1.01)

# ── 2D image ──────────────────────────────────────────────
kw = dict(aspect="auto", cmap=CI, vmin=0, vmax=1, origin="lower")
im6 = ax6t.imshow(img_top,
                  extent=[z_caus_mm[0], z_caus_mm[-1], 0, r_show], **kw)
ax6t.imshow(img_bot,
            extent=[z_caus_mm[0], z_caus_mm[-1], -r_show, 0],
            origin="upper", aspect="auto", cmap=CI, vmin=0, vmax=1)

ax6t.plot(z_caus_mm,  w_th, "#4fc3f7", lw=2)
ax6t.plot(z_caus_mm, -w_th, "#4fc3f7", lw=2)

draw_tubes(ax6t, -tube_r_um, tube_r_um, label=False)

for sgn in (+1, -1):
    ax6t.axvline(sgn * zR_mm, color="#ffd54f", lw=1.2, ls="--", alpha=0.85)
ax6t.text( zR_mm + 0.4,  r_show * 0.88, f"z_R = {zR_mm:.1f} mm",
           color="#ffd54f", fontsize=9)
ax6t.text(-zR_mm - 0.4,  r_show * 0.88, f"−z_R",
           color="#ffd54f", fontsize=9, ha="right")

cb6 = plt.colorbar(im6, ax=ax6t, fraction=0.020, pad=0.01)
cb6.ax.tick_params(labelsize=7, colors="#888")

ax6t.set_ylabel("r [µm]", fontsize=11)
ax6t.set_ylim(-r_show, r_show)
ax6t.tick_params(labelbottom=False, colors="#888")
ax6t.set_facecolor("#0e1117")

# ── w(z) line plot ────────────────────────────────────────
ax6b.plot(z_caus_mm, w_caus, "#ffffff", lw=2, label="Simulated")
ax6b.plot(z_caus_mm, w_th,  "--", color="#ff7043", lw=1.5, alpha=0.8,
          label=r"$w_0\sqrt{1+(z/z_R)^2}$")
ax6b.axhline(w0_f_um, color="#a5d6a7", lw=1.2, ls=":", alpha=0.9,
             label=f"w₀ = {w0_f_um:.0f} µm")

ax6b.axvline( zR_mm, color="#ffd54f", lw=1.2, ls="--", alpha=0.85)
ax6b.axvline(-zR_mm, color="#ffd54f", lw=1.2, ls="--", alpha=0.85)

draw_tubes(ax6b, 0, tube_r_um)

ax6b.text(zR_mm + 0.4,  w_caus.max() * 0.65,
          f"z_R\n{zR_mm:.1f} mm", color="#ffd54f", fontsize=9)
ax6b.text(-zR_mm - 0.4, w_caus.max() * 0.65,
          f"−z_R", color="#ffd54f", fontsize=9, ha="right")

ax6b.set_xlabel("z from focus [mm]", fontsize=11)
ax6b.set_ylabel("w(z) [µm]", fontsize=11)
ax6b.legend(fontsize=9, facecolor="#1a1a2e", labelcolor="#ddd", loc="upper right")
ax6b.grid(True, alpha=0.2)
ax6b.set_facecolor("#0e1117")

plt.savefig("fig6_beam_evolution.png", dpi=150, bbox_inches="tight",
            facecolor="#0e1117")
print("  Saved: fig6_beam_evolution.png")

plt.show()
print("\n  Done.")
