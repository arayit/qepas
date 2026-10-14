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

## Pump fallbacks

- **Peristaltic pump with Viton (FKM) tubing.** Often already in the lab;
  10–200 mL/min, adjustable; only the tubing touches the gas; pulsation is far
  below 12.46 kHz and is rejected by the lock-in.
- **EPDM micro diaphragm pump** (e.g. KNF NMP 03 / NMP 05, 0.33 / 0.45 L/min).
  Acceptable for a short PoC only: run a blank (no dosing) before each test to
  check carry-over, and do not use it for absolute calibration.

## Open items

- Quantitative methyl salicylate spectrum (PNNL/NWIR or DTIC ADA392033) for a
  real cross-section and LOD.
- Neumo items that depend on the pump's port type (reducing union, hose).
- Prior art to cite: CREO GC-QEPAS measured methyl salicylate as a CWA
  simulant (Zampolli et al. 2020, Sensors 20:120; Liberatore et al. 2025,
  Forensic Sci. Res. 10). Their 60 L test chamber with µL syringe dosing onto a
  ~40 °C crucible is a citable precedent for our dosing.
