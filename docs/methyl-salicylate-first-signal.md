# Methyl salicylate — first signal, then the chamber

Status, 14 Oct 2026: the pump offers (Schwarzer SP 240 EC-LC-SO, Xavitech
P200) did not work out, so the closed-loop chamber waits for a pump. Time is
short and the immediate goal is to see a methyl salicylate signal on the ADM.

## Step 0 — first signal with the existing flow-through line

No new pump is needed. Use the line that detected N2O in exp6, with one glass
vessel added:

```
N2 → MFC → glass bottle with methyl salicylate → PCD → ADM → needle valve → Vacuubrand pump
```

1. A few drops of methyl salicylate (≥99 %, reagent grade) in a small glass
   bottle with a two-port cap, e.g. 100 mL bottle with a GL45 HPLC cap.
2. Bottle sits after the MFC, so the MFC meters clean N2 only.
3. Operate as in exp6: ~10 sccm, 205 Torr, needle valve after the ADM.
4. MIRcat at 1304.7 cm-1 (methyl salicylate 1310 band; 7 cm-1 from N2O R15,
   so laser, optics and water background are known).
5. Two runs at the same wavelength: N2 direct, then N2 through the bottle.
6. Short scan ~1290–1320 cm-1. A broad, smooth band confirms methyl
   salicylate rather than sharp water or N2O lines.

Expected (estimate — no quantitative methyl salicylate spectrum yet):

| Quantity | Value |
|---|---|
| Saturated headspace, 25 °C | ~45 ppm |
| Responsivity, N2O R15 as stand-in | 0.20 mV/ppm |
| Rough signal | ~9 mV |
| Blank noise (exp9) | 0.12 mV |

A sweep over the liquid may not fully saturate; the signal is still expected
well above noise even if the true responsivity is 10× lower. Pump exhaust is a
few ppm at 10 sccm; route it to a fume hood if available.

This run also gives the first responsivity estimate for methyl salicylate.

## Step 1 — closed-loop chamber, once a pump is found

```
1 L jar → particle filter → PCD (dead-end tee) → ADM → pump → MFC / needle valve → jar
```

- Throttling always after the pump, so the ADM stays at chamber pressure.
- Start at the validated 10 sccm, then step 30 → 100 → 200 sccm and record
  noise at each step. The highest flow without extra noise is the working flow.
- Wetted parts glass, stainless steel, PTFE; elastomers FKM or better where
  possible (see pump fallbacks).

## Pump options (updated 20 Oct 2026)

Rejected: Schwarzer SP 240 EC-LC-SO (EPDM only), Xavitech P200 (bulk only).
No reply yet: TCS Micropumps direct.

| # | Pump | Flow | Wetted parts | Motor | Single unit |
|---|---|---|---|---|---|
| 1 | TCS D260BLX-V, via RS Components (ref. 8170716) or Servoflo | ~400 mL/min | FKM, 316 SS head | Brushless, 3–6 V | Yes, ~£120 |
| 2 | Sensidyne AAA series | 235–1410 cc/min | Viton diaphragm option | Brushless option, 3/6/12 V | To confirm |
| 3 | Hilintec S23 | ≥0.85 L/min | FKM diaphragm and valves, PA6 head | Brushless, 12 V | To confirm |
| 4 | Bodenpump BD-05T01.51500B | 1–1.5 L/min | EPDM std, FKM option | Brushless | To confirm |
| 5 | Perimax PMP216V peristaltic, Viton tube | ≤35 mL/min | Viton tube only | 12 V | Yes, ~$94 |

Notes:
- 5 covers only the first low-flow steps (10–30 sccm), not 200 sccm. A lab
  peristaltic drive with Masterflex L/S 16 Viton tubing covers the full range.
- Eliminated: Boxer (FKM only on the 18 L/min 3KD; 22K is EPDM/silicone),
  Cole-Parmer catalogue pumps (all ≥ several L/min), Senior Metal Bellows
  MB-21 (all-steel, ideal materials, but ~5.7 slm and ~$2000+).
- Last resort for a short PoC only: an EPDM micro pump, with a blank run before
  every test and no absolute calibration.

## Open items

- Quantitative methyl salicylate spectrum (PNNL/NWIR or DTIC ADA392033) for a
  real cross-section and LOD.
- Neumo items that depend on the pump's port type (reducing union, hose).
- Prior art to cite: CREO GC-QEPAS measured methyl salicylate as a CWA
  simulant (Zampolli et al. 2020, Sensors 20:120; Liberatore et al. 2025,
  Forensic Sci. Res. 10). Their 60 L test chamber with µL syringe dosing onto a
  ~40 °C crucible is a citable precedent for our dosing.
