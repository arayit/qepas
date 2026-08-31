# Band selection from measured gas-phase spectra

Source: NIST WebBook / Sadtler-EPA gas-phase IR, 4 cm-1 step, `##STATE=gas`.
Water: HITRAN, 14.0 Torr H2O (lab air at 21 C / 75% RH per the exp7 operator
log), 205 Torr total, 0.26 cm-1 laser, mV via the R14 responsivity anchor.

**These spectra carry no path length or concentration**, so the absorbance
scale is arbitrary. Band positions, relative strengths *within* one compound,
and all water numbers are real. Absolute cross-sections, mV/ppm and LOD are
not available until quantitative (PNNL) data is in hand — and strengths cannot
be compared *between* compounds from these files.

## Ethyl acetate (CAS 141-78-6) — Step 1 test compound

| Band | Rel. | H2O at peak | Best set point | Rel. there | H2O there |
|---|---|---|---|---|---|
| **1238** | **1.00** | **0.00 mV** | **1232.46** | 0.92 | **0.000 mV** |
| 1770 (C=O) | 0.67 | 11.36 mV | 1755.00 | 0.61 | 3.24 mV |
| 1374 | 0.22 | 343 mV | 1381.19 | 0.21 | 0.29 mV |

The acetate C–O–C at 1238 is both the **strongest in-window band and
water-free**. Use it. The carbonyl is weaker *and* sits in water — exactly the
trade the band-position reasoning predicted.

## Methyl salicylate (CAS 119-36-8) — candidate real target

| Band | Rel. | H2O at peak | Best set point | Rel. there | H2O there |
|---|---|---|---|---|---|
| **1310** | **1.00** | 0.13 mV | **1304.71** | 0.91 | **0.026 mV** |
| 1698 (C=O) | 1.00 | 42.55 mV | 1703.17 | 0.91 | 20.51 mV |
| 1214 | 0.73 | 0.03 mV | 1208.74 | 0.66 | 0.010 mV |
| 1254 | 0.55 | 0.00 mV | 1250.28 | 0.54 | 0.003 mV |
| 1166 | 0.46 | 0.82 mV | 1157.64 | 0.45 | 0.000 mV |

Three strong clean bands (1310, 1214, 1254) and one strong dirty one (1698).
**1310 is the pick**: joint-strongest and essentially water-free.

Note how close that is to the N2O work — R15 sits at 1297.8314, so 1310 is
only ~12 cm-1 away, in a region whose water background is already
characterised from exp4/exp7.

## Method note

A broad band can be *slid* into a water gap: moving ethyl acetate's set point
1238 -> 1232.46 costs 8% of signal, and moving methyl salicylate's C=O
1698 -> 1703.17 halves its water for 9%. A sharp line like R15 is pinned to
its centre; a 30 cm-1 band is not. The `H2O +-` column in
`analysis/voc_band_ranking.py` checks the gap is wider than the laser's
set-point reproducibility before trusting it.

## Still needed

- (Z)-3-hexenyl acetate — the GLV ester, not yet pulled
- Quantitative spectra (PNNL/NWIR, or DTIC ADA392033 for methyl salicylate)
  to turn these into cross-sections, calibration slopes and detection limits
