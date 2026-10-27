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


## (Z)-3-hexenyl acetate (CAS 3681-71-8) — the GLV ester from cut grass

**No gas-phase IR in NIST** (checked 27 Oct 2026: the WebBook entry has only
MS and GC data; the (E)-2 isomer likewise). Two substitutes:

1. **n-Hexyl acetate (CAS 142-92-7), NIST gas phase** — same acetate group on a
   saturated C6 chain. File `hexyl_acetate.csv`. Ranked exactly like ethyl
   acetate: strongest band 1238, best set point **1232.46**, water **0.000 mV**
   (205 Torr, 14 Torr H2O), FWHM 32 cm-1.
2. **(Z)-3-hexenyl acetate itself, liquid ATR** (SpectraBase JY3GdO5RDHr via
   PubChem CID 5363388): tallest peak **≈1233 cm-1**; the capillary-film FTIR
   (9jzzCTGPimz) has its C=O at ≈1735. Gas-phase bands of esters sit within a
   few cm-1 of the liquid, so the acetate band is expected at 1233 ± 5 in the
   gas. Our 1232.46 set point is inside the band top either way; the final set
   point is chosen by scanning the real compound in the bottle test.

Figure: `figures/hexyl_acetate_nist.{pdf,png}`.

**Why this is the PoC compound.** It is what the plant emits after cutting, so
the dosed calibration and the wound burst are the same molecule:

- D'Auria et al. 2007, *Plant J.* 49:194 — in Arabidopsis "upon mechanical
  damage, the (Z)-3-hexen-1-yl acetate emission peaked after 5 min and
  declined to pre-damage levels after 90 min"; the early ester comes from CHAT
  enzyme already present in the leaf.
- Ameye et al. 2018, *New Phytol.* 220:666 (p. 675) — hexenal "peaked 5 min
  after wounding, declined rapidly and coincided with an increase of hexenyl
  alcohols and acetates" (citing Fall et al. 1999); wounded Arabidopsis released
  more Z-3-HAC than herbivore-attacked plants.
- Tholl et al. 2006, *Plant J.* 45:540 — lists "(Z)-3-hexenal and
  (Z)-3-hexenyl acetate" as the typical C6 green-leaf volatiles.
- Caveat: Brilli et al. 2011 (PTR-TOF, *Dactylis*) report the acetates as the
  slowest, last GLVs after wounding. Timing differs by species; cat grass is a
  grass like *Dactylis*, so expect the ester to lag the aldehyde by minutes.

Safety: FEMA GRAS 3171, GHS H226 only, no OSHA limit, flash point 57 °C.

## Method note

A broad band can be *slid* into a water gap: moving ethyl acetate's set point
1238 -> 1232.46 costs 8% of signal, and moving methyl salicylate's C=O
1698 -> 1703.17 halves its water for 9%. A sharp line like R15 is pinned to
its centre; a 30 cm-1 band is not. The `H2O +-` column in
`analysis/voc_band_ranking.py` checks the gap is wider than the laser's
set-point reproducibility before trusting it.

## Still needed

- Quantitative spectra (PNNL/NWIR, or DTIC ADA392033 for methyl salicylate)
  to turn these into cross-sections, calibration slopes and detection limits
