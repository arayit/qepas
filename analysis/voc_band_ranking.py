#!/usr/bin/env python3
"""Rank candidate plant VOCs for QEPAS detection in the MIRcat window.

Companion to the thesis repo's analysis/full_band_line_ranking.py, which does
the same job for sharp N2O lines. The difference that matters works in our
favour: a VOC band is 20-40 cm-1 wide and flat near its top, so the set point
can be slid several cm-1 to land in a water gap while keeping nearly full
analyte signal. A sharp line like R15 is pinned to its centre; a broad band is
not. This script therefore searches *within* each band for the set point that
maximises the analyte-to-water ratio, rather than defaulting to the peak.

Input
  data/pnnl/<compound>.csv   two columns: wavenumber [cm-1], absorbance
                             PNNL/NWIR convention = base-10 absorbance
                             normalised to 1 ppm-m at 1 atm, 296 K.
                             Header row optional; comma or whitespace.
  HITRAN .par with H2O lines (--par), e.g. the thesis repo's
  data/hitran/h2o_n2o_1111-2000_hitran.par

Output (stdout)
  Per compound: peak position, band FWHM, peak cross-section, predicted
  calibration slope, water background under the band, rejection ratio,
  predicted LOD, and a proposed on-band / off-band set-point pair.

Usage
  python3 voc_band_ranking.py --pnnl data/pnnl --par path/to/h2o.par
"""
import argparse
import sys
from pathlib import Path

import numpy as np

# ── PNNL absorbance -> cross-section ──────────────────────────────────
# PNNL absorbance A is base-10, for a burden of 1 ppm-m at 1 atm, 296 K.
# Column density for 1 ppm-m = n(1 atm, 296 K) * 1e-6 * 100 cm = 2.479e15 cm-2
# sigma_e = ln(10) / 2.479e15 * A
PNNL_TO_SIGMA = 9.287e-16      # cm^2/molecule per unit PNNL absorbance

# ── operating point (edit to match the session being modelled) ────────
P_TORR = 205.0                 # exp6/exp9 flow-mode pressure
T_K = 298.0
W_FWHM = 0.26                  # fitted pulsed-laser lineshape FWHM, cm-1
B_RESP = 51788.0               # mV per cm-1 of alpha (R14 responsivity anchor,
                               # fitted at 600 Torr — see caveat in output)
NOISE_MV = 0.12                # 1-sigma blank noise, mV (exp9 blank spread)
TUNE_REPRO = 0.05              # set-point reproducibility, cm-1. exp78 put it
                               # at ~0.01; 0.05 is a deliberately pessimistic
                               # margin for judging whether a water gap is
                               # actually usable session to session.
WINDOW = (1111.0, 2000.0)      # MIRcat tuning range

N_TOT = (P_TORR / 760.0) * 101325 / (1.380649e-23 * T_K) * 1e-6   # cm^-3


def load_voc(path):
    """Tolerant two-column loader: comma or whitespace, header optional."""
    nu, ab = [], []
    for line in open(path):
        line = line.strip()
        if not line or line.startswith(("#", "//")):
            continue
        parts = line.replace(",", " ").split()
        if len(parts) < 2:
            continue
        try:
            x, y = float(parts[0]), float(parts[1])
        except ValueError:
            continue                      # header row
        nu.append(x)
        ab.append(y)
    if not nu:
        raise ValueError(f"no numeric rows in {path}")
    nu, ab = np.asarray(nu), np.asarray(ab)
    order = np.argsort(nu)
    return nu[order], ab[order]


def load_water(par_path):
    """H2O lines (molecule id 1) from a HITRAN .par file."""
    out = []
    for l in open(par_path):
        if len(l) < 120 or int(l[0:2]) != 1:
            continue
        out.append((float(l[3:15]), float(l[15:25]), float(l[35:40])))
    return out


def water_alpha(grid, lines, p_h2o_torr):
    """Lorentzian-broadened water absorption on `grid`, cm-1."""
    conc = p_h2o_torr / P_TORR
    a = np.zeros_like(grid)
    for nu0, S, g_air in lines:
        if not (grid[0] - 6 < nu0 < grid[-1] + 6):
            continue
        g = max(g_air, 0.02) * (P_TORR / 760.0)
        m = np.abs(grid - nu0) < 6.0
        a[m] += S * conc * N_TOT * g / (np.pi * ((grid[m] - nu0) ** 2 + g ** 2))
    return a


def convolve_laser(a, step):
    sig = W_FWHM / 2.3548 / step
    n = int(6 * sig) + 1
    k = np.exp(-0.5 * (np.arange(-n, n + 1) / sig) ** 2)
    return np.convolve(a, k / k.sum(), mode="same")


def band_fwhm(nu, sig, peak_i):
    """Full width at half max around the peak, cm-1 (nan if not enclosed)."""
    half = sig[peak_i] / 2.0
    left = right = None
    for i in range(peak_i, 0, -1):
        if sig[i] < half:
            left = nu[i]
            break
    for i in range(peak_i, len(sig)):
        if sig[i] < half:
            right = nu[i]
            break
    return right - left if (left is not None and right is not None) else np.nan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pnnl", default="data/pnnl",
                    help="directory of <compound>.csv spectra")
    ap.add_argument("--par", default=None,
                    help="HITRAN .par containing H2O lines")
    ap.add_argument("--ph2o", type=float, default=14.0,
                    help="water partial pressure, Torr (default 14.0 = "
                         "lab air at 21 C, 75%% RH, exp7 operator log)")
    args = ap.parse_args()

    files = sorted(Path(args.pnnl).glob("*.csv"))
    if not files:
        sys.exit(f"no .csv spectra found in {args.pnnl}")

    print(f"conditions: {P_TORR:.0f} Torr, {T_K:.0f} K, laser FWHM "
          f"{W_FWHM} cm-1, p(H2O) {args.ph2o} Torr")
    print(f"window: {WINDOW[0]:.0f}-{WINDOW[1]:.0f} cm-1\n")

    wlines = load_water(args.par) if args.par else []
    if args.par:
        print(f"water: {len(wlines)} H2O lines loaded\n")
    else:
        print("water: no --par given, water columns will be blank\n")

    rows = []
    for f in files:
        nu, ab = load_voc(f)
        m = (nu >= WINDOW[0]) & (nu <= WINDOW[1])
        if not m.any():
            print(f"  ! {f.stem}: no data inside the window, skipped")
            continue
        nu, ab = nu[m], ab[m]
        sigma = ab * PNNL_TO_SIGMA

        i = int(np.argmax(sigma))
        nu_pk, sig_pk = nu[i], sigma[i]
        fwhm = band_fwhm(nu, sigma, i)

        step = 0.002
        span = max(fwhm if np.isfinite(fwhm) else 30.0, 10.0)
        grid = np.arange(nu_pk - span - 30, nu_pk + span + 30, step)
        wa = (convolve_laser(water_alpha(grid, wlines, args.ph2o), step)
              if wlines else np.zeros_like(grid))
        voc_on_grid = np.interp(grid, nu, sigma, left=0.0, right=0.0)

        # Search within the band top for the best set point: keep at least
        # KEEP of the peak analyte signal, then minimise water. This is the
        # freedom a broad band buys us that a sharp line does not have.
        KEEP = 0.90
        ok = voc_on_grid >= KEEP * sig_pk
        if ok.any():
            k_grid = voc_on_grid * 1e-6 * N_TOT * B_RESP
            w_grid = wa * B_RESP
            score = np.where(ok, k_grid / np.maximum(w_grid, 1e-6), -np.inf)
            j = int(np.argmax(score))
            nu_on = float(grid[j])
            k_mv_ppm = float(k_grid[j])
            w_mv = float(w_grid[j])
        else:
            nu_on = nu_pk
            k_mv_ppm = sig_pk * 1e-6 * N_TOT * B_RESP
            w_mv = float(np.interp(nu_pk, grid, wa)) * B_RESP

        # water penalty paid by naively sitting on the band peak
        w_peak = float(np.interp(nu_pk, grid, wa)) * B_RESP

        # robustness: worst water within the laser's set-point reproducibility.
        # A gap narrower than TUNE_REPRO is not a gap you can actually use.
        near = np.abs(grid - nu_on) <= TUNE_REPRO
        w_worst = float(np.max(wa[near])) * B_RESP if near.any() else w_mv

        # off-band: nearest point where the analyte has fallen below 5% of
        # peak AND water is low, so only the flat optical background remains
        off_nu = np.nan
        faint = (voc_on_grid < 0.05 * sig_pk)
        if faint.any():
            cand = np.where(faint & (wa * B_RESP < max(w_mv * 2, 0.5)))[0]
            if cand.size:
                off_nu = float(grid[cand[np.argmin(np.abs(grid[cand] - nu_on))]])

        lod3 = 3 * NOISE_MV / k_mv_ppm if k_mv_ppm > 0 else np.inf
        rows.append(dict(name=f.stem, nu=nu_on, peak=nu_pk, fwhm=fwhm,
                         sigma=sig_pk, k=k_mv_ppm, w=w_mv, wpk=w_peak,
                         wworst=w_worst, lod=lod3, off=off_nu,
                         ratio=k_mv_ppm / w_mv if w_mv > 1e-6 else np.inf))

    def rank(r):
        rr = r["k"] / r["wworst"] if r["wworst"] > 1e-6 else float("inf")
        return -(rr if np.isfinite(rr) else 1e9 + r["k"])
    rows.sort(key=rank)

    hdr = (f"{'compound':<24}{'on-band':>9}{'FWHM':>7}{'sigma':>11}"
           f"{'mV/ppm':>9}{'H2O mV':>9}{'H2O+-':>9}{'ratio':>9}"
           f"{'LOD3s':>8}{'off-band':>10}{'H2O@peak':>10}")
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        rr = r["k"] / r["wworst"] if r["wworst"] > 1e-6 else float("inf")
        ratio = "inf" if not np.isfinite(rr) else f"{rr:.0f}"
        print(f"{r['name']:<24}{r['nu']:9.2f}{r['fwhm']:7.1f}"
              f"{r['sigma']:11.2e}{r['k']:9.4f}{r['w']:9.3f}"
              f"{r['wworst']:9.3f}{ratio:>9}{r['lod']:8.2f}"
              f"{r['off']:10.2f}{r['wpk']:10.2f}")

    print("\nunits: cm-1 for wavenumbers, sigma cm2/molecule, LOD3s ppm "
          "at the stated noise")
    print(f"on-band = best set point within the band top (>=90% of peak "
          f"analyte signal). H2O+- = worst water within +-{TUNE_REPRO} cm-1 "
          f"of it, i.e. what you actually get session to session; ratio and "
          f"the ranking use that, not the best-case value. H2O@peak = what "
          f"you would pay by naively sitting on the band maximum.")
    print("caveat: B_RESP is the R14 responsivity anchor fitted at 600 Torr; "
          "at 205 Torr Q is higher, so absolute mV/ppm carries the anchor's "
          "+-30-40% systematic. Rankings and ratios are unaffected.")


if __name__ == "__main__":
    main()
