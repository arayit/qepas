# Choosing a plant-VOC sampling method for the QEPAS ADM

A review of five papers on plant volatile sampling, read against the physical
constraints of our Acoustic Detection Module, with a concrete recommendation.

**Papers reviewed**

| # | Reference |
|---|---|
| P1 | Tholl et al. (2006) *Practical approaches to plant volatile analysis*, Plant J. 45, 540–560 |
| P2 | Tholl et al. (2021) *Trends and applications in plant volatile sampling and analysis*, Plant J. 106, 314–325 |
| P3 | Liu et al. (2023) *VOCs from plants: from release to detection*, TrAC 158, 116872 |
| P4 | Li et al. (2019) *Non-invasive plant disease diagnostics enabled by smartphone-based fingerprinting of leaf volatiles*, Nat. Plants 5, 856–866 |
| P5 | Li et al. (2021) *Real-time monitoring of plant stresses via chemiresistive profiling of leaf volatiles by a wearable sensor*, Matter 4, 2553–2570 |

---

## 1. What the ADM actually demands from a sampling front end

Geometry taken from `beam_propagation.py`:

| Parameter | Value |
|---|---|
| Microresonator tubes | 2 × Ø 1.6 mm × 12.4 mm, gaps 0.1 / 0.3 mm from focus |
| Bore volume | 24.9 µL per tube, **49.9 µL total** |
| Wavelength | 7.6 µm (1316 cm⁻¹) |
| OAP | RFL 25.4 mm, Ø 25.4 mm, input w₀ = 2.5 mm at 200 mm |

Five properties of QEPAS decide which literature method can be adapted:

1. **No preconcentration.** The signal is proportional to the analyte concentration
   *present in the bore at that instant*. Unlike every GC-coupled method in P1–P3,
   there is no adsorb-and-desorb gain stage. Whatever the sampling scheme delivers
   is what gets measured.
2. **Very small volume.** 50 µL of resonator; a ~2 mL housing exchanges in 4 s at
   30 sccm (0.1 s for the resonators alone). This is a genuine advantage — the ADM
   does not need a large sample and does not need high flow for time resolution.
3. **Low flow ceiling.** The QTF is a microphone. Flow noise at the tube ends and
   diaphragm-pump pulsation couple directly into the signal, so the practical
   operating range is ~10–100 sccm with buffer volumes and a mechanically decoupled
   pump. Note the tube length: 12.4 mm is λ/4 at ≈6.9 kHz and λ/2 at ≈13.8 kHz, so
   this is a **custom low-frequency QTF, not a 32.768 kHz one** (inference from
   geometry — worth confirming). Low-frequency QTFs are more exposed to ambient
   acoustic and flow noise, which tightens the flow budget further.
4. **Humidity dependence.** Water vapour is a V–T relaxation promoter; QEPAS
   response for many molecules changes with RH. RH must be *fixed*, not merely
   tolerated. Both sensor papers already do this — P4 and P5 both condition their
   test streams to 50% RH by mixing saturated vapour with dry and wet carrier at
   500 sccm.
5. **Wall adsorption.** The most-cited disease markers include semi-volatiles
   (methyl salicylate, methyl jasmonate, 2-phenylethanol, 4-ethylphenol). Lines
   must be short, glass/PTFE, and gently heated.

Together these say: the front end must deliver a **small, low-flow, humidity-conditioned,
high-concentration** stream. That is the opposite of what a conventional 1–4 L plant
chamber flushed at litres per minute produces.

---

## 2. Method inventory across the five papers

| Method | Source | Native output | Fit to ADM |
|---|---|---|---|
| Static headspace + SPME | P1 §static, P2, P3 §4.1 | Loaded fibre → GC injector | **Poor.** Thermal desorption into a GC is intrinsic; one-shot; quantitation weak (P2 Table 1). |
| SBSE / "Twister", PDMS tubing | P2 | Loaded sorbent → TD unit | **Poor**, same reason. Higher capacity than SPME but still GC-bound. |
| Needle-trap microextraction | P2 (Beck 2015) | Sorbent needle → GC injector | **Adaptable** as a preconcentrator (see Stage E). |
| Micro-preconcentrator chip | P2 (McCartney 2017) | Flash-desorbed plug; 22 ppb with 2-min load | **Good** bolt-on gain stage. |
| Dynamic "pull" | P1 Fig. 4a,b | Continuous flow through a trap | Workable but ambient-air contamination is high (P1). |
| Dynamic **push–pull** | P1 Fig. 4c,d; P2 Fig. 1 | Continuous, defined sub-flow through a trap | **Very good.** The trap position maps 1:1 onto the ADM. |
| **Closed-loop stripping** | P1 Fig. 3 (Boland 1984; Donath & Boland 1995) | Recirculating closed volume, trap in loop | **Best fit** once the trap is removed — see §3. |
| Gas-exchange cuvettes | P1 §cuvettes; P2 (VOC-SCREEN, Jud 2018) | Flow-through leaf/branch enclosure, split to detectors | **Very good** as the enclosure for either of the above. |
| Sealed vial + micropump sweep | P4 Methods | 20 mL vial, 1 h accumulation, 480 sccm sweep | **Good** as a fast first protocol. |
| Leaf-clamp micro-chamber | P5 | <2 cm³ gap on an intact leaf, 0.6 mm spacer | **Excellent** enclosure concept; smallest volume in the set. |

P1 already notes that laser IR photoacoustic spectroscopy detects isoprene "down to
a few ppbv with a time resolution of 1 min in a continuous gas stream" and calls for
smaller instruments — our ADM is the answer to that 2006 complaint, so the method
choice should play to the strength it adds (real time, in situ) rather than imitate
a GC workflow.

---

## 3. The concentration arithmetic — why the closed loop wins

For an emission rate *E* (nmol min⁻¹) at 1 atm, 25 °C:

```
open flow, steady state:     C[ppm] = 24.45 · E / F          (F in mL/min)
closed loop, accumulating:   C[ppm] = 24.45 · E · t / V      (V in mL, t in min)
```

**Open flow-through** — concentration is set by dilution and never improves:

| F (mL/min) | E = 0.06 | E = 0.6 | E = 6.0 nmol/min |
|---|---|---|---|
| 20 | 0.073 ppm | 0.73 ppm | 7.3 ppm |
| 100 | 0.015 ppm | 0.15 ppm | 1.5 ppm |
| 500 | 0.003 ppm | 0.029 ppm | 0.29 ppm |
| 1000 | 0.0015 ppm | 0.015 ppm | 0.15 ppm |

**Closed loop** — concentration climbs linearly with time, and inversely with loop volume:

| V (mL) | t (min) | E = 0.06 | E = 0.6 | E = 6.0 nmol/min |
|---|---|---|---|---|
| 2 | 15 | 11.0 ppm | 110 ppm | 1100 ppm |
| 20 | 15 | 1.10 ppm | 11.0 ppm | 110 ppm |
| 20 | 60 | 4.40 ppm | 44.0 ppm | 440 ppm |
| 100 | 30 | 0.44 ppm | 4.40 ppm | 44.0 ppm |
| 1000 | 30 | 0.044 ppm | 0.44 ppm | 4.40 ppm |

**Sanity check against P4.** Li et al. sealed a detached leaf in a 20 mL vial and let
the headspace accumulate for 1 h. Our model predicts 4.4 ppm for a weakly emitting
leaf; they measured 0.3–18 ppm across six markers in infected potato tissue
((E)-2-hexenal 12–18 ppm, (Z)-3-hexenal 6–12, hexanal 3–6, 4-ethylphenol 3–6,
2-phenylethanol 1.5–3, benzaldehyde 0.3–1.5). The arithmetic reproduces their
measured range, so it can be trusted for sizing.

**The conclusion is stark:** for the same plant, a 2 mL closed loop after 15 minutes
delivers ~750× the concentration of a 1 L/min open chamber. Shrinking the enclosure
and closing the loop are worth far more than any improvement we can make to the ADM
electronics.

---

## 4. Recommendation

> **Adapt the closed-loop stripping method of Boland (1984) / Donath & Boland (1995),
> as described in P1 §"Closed-loop stripping" and Fig. 3 — with the adsorbent
> cartridge removed and the ADM put in its place, and the 1–3 L desiccator replaced
> by a leaf cuvette (P1 §cuvettes) or the leaf-clamp micro-chamber geometry of P5.**

The original method circulates headspace air at 2–3 L/min through a charcoal trap in a
1 L desiccator for 8 h. Every element transfers, with one inversion: **we delete the
trap**, because the ADM *is* the detector, and the loop then stops being a transport
path and becomes an accumulation cell.

Why this one:

- It is the only method in this literature whose native output is *a rising gas-phase
  concentration inside a small closed volume* — precisely what a non-preconcentrating,
  small-volume, real-time detector wants.
- P1 gives its motivation directly: closed-loop stripping "is applicable to VOC
  analyses of plants with low volatile emissions" and shows "a significantly higher
  signal to noise ratio due to the trapping of fewer air contaminants". For a
  background-limited absorption technique, excluding ambient air is worth as much
  as the concentration gain.
- The slope d*C*/d*t* **is** the emission rate. A linear fit over the accumulation
  gives a quantitative result that is robust against the ADM's absolute calibration
  drifting — a much better observable than a single steady-state reading.
- Loop volume is a free design parameter we control, and §3 shows it is the dominant
  one.

### Staged plan

**Stage A — bench calibration (before any plant).** Reproduce the gas-standard rig
from P4/P5 Methods: mass flow controllers blending saturated analyte vapour with dry
and wet carrier to give 0.1–100 ppm at fixed 50% RH. Measure the ADM's real LOD and
its RH response curve for the chosen marker. Everything downstream depends on this
number.

**Stage B — fastest first plant data: P4's vial protocol.** Detached leaf in a 20 mL
borosilicate scintillation vial, Parafilm-sealed, 1 h at 95% RH, then sweep the
headspace through the ADM with zero air. Use a sample loop / 6-port valve and
integrate the transient peak. This reaches 0.3–18 ppm, comes with a validated disease
model (*P. infestans* on tomato, sporangia ~10⁴ mL⁻¹), and gives SPME-GC-MS ground
truth for free.

**Stage C — the primary method: trap-less closed-loop micro-cuvette.** Leaf clamp,
recirculation pump, ADM, and the shortest possible PTFE tubing, total loop volume
2–20 mL. Follow P5's mechanical solution for the clamp: a 0.6 mm double-sided-tape
spacer holding the chamber off the leaf surface, exploiting trichomes to prevent
contact — they achieved <2 cm³ this way on a living tomato leaf. Record C(t) for
10–30 min, fit the slope, then vent and repeat. P5 also demonstrates the robustness
that matters in practice: their leaf-mounted chamber was insensitive to 1.5 m s⁻¹
wind, to touching the stem, and to watering events.

**Stage D — the cross-check: push–pull open flow (P1 Fig. 4c).** Not optional. P1
explicitly warns that "results from closed-loop stripping sampling should always be
compared with those obtained by open headspace trapping to exclude artifacts due to
effects on the enclosed plant caused by changes in the atmosphere of the chamber",
and specifically flags accumulating humidity and untrapped compounds. Build the
push–pull chamber with charcoal-filtered air in, the ADM on the pull arm in the
adsorbent trap's position, and a vent for the balance. It also gives the true zero-gas
baseline the ADM needs, and lets the incoming humidity be set deliberately.

**Stage E — only if Stage A says sensitivity is short.** Add the micro-preconcentrator
of McCartney et al. (cited in P2): sorbent chip with integrated heater, load for
2 min at ~50 sccm, flash-desorb into a ~1 mL zero-air plug through the ADM. They
reached 22 ppb with FID at a 2-min load; the same gain stage in front of the ADM
buys 2–3 orders of magnitude.

### Design targets

| Parameter | Target | Rationale |
|---|---|---|
| Loop volume | 2–20 mL total | §3; dominant sensitivity lever |
| Recirculation flow | 20–50 sccm | Above flow-noise threshold concerns, ≥1 loop turnover/s |
| Pump | Decoupled, with buffer volume both sides | QTF is a microphone; P4's 480 sccm diaphragm pump would be far too pulsatile as-is |
| Materials | Glass / PTFE only, no Tygon | P1: avoid materials that retain volatiles or bleed |
| Line temperature | ~40 °C | Semi-volatile markers |
| RH | Fixed and logged | QEPAS relaxation dependence |
| Accumulation | 10–30 min, then vent | P1's warning on closed-chamber artifacts |
| Cuvette turnover | ≥2 × per minute | P1: prevents boundary layer and condensation — trivially met by a small loop |

---

## 5. Open issues to resolve

1. **Spectral match at 7.6 µm — check this first.** 1316 cm⁻¹ is the classic
   CH₄ ν₄ / N₂O region; it is not obviously where the green-leaf-volatile and
   phytohormone markers of P4/P5 have their strongest bands (aldehyde C=O sits near
   1730 cm⁻¹, ethylene at 949 cm⁻¹, methanol's strong C–O near 1033 cm⁻¹). Before
   committing to a sampling geometry, pull the HITRAN/PNNL cross-sections for the
   intended target at 7.6 µm. The sampling recommendation above is independent of
   which marker is chosen, but the required loop volume is not.
2. **One wavelength vs. a fingerprint.** All five papers frame plant-VOC diagnostics
   as *multivariate* — P4 discriminates 10 volatiles, P5 discriminates 13, both by
   PCA/LDA over a sensor array, and both state that single-compound correlation to
   disease status is weak. A single-λ QEPAS returns one number. Either commit to one
   well-chosen marker with a clean band, or plan for a swept EC-QCL / multi-source
   ADM. This is the largest strategic gap between our instrument and this literature.
3. **Beam clipping in the microresonator.** With w₀ = 2.5 mm at the OAP and
   RFL = 25.4 mm, the focal waist is 24.5 µm with a Rayleigh range of only 0.25 mm.
   The beam radius reaches the 800 µm tube wall at **z ≈ 8.1 mm**, while each tube
   extends to 12.7 mm from focus. Roughly the outer third of each tube is illuminated
   at its wall, which will generate a large spurious photoacoustic background and
   raise the noise floor the sampling design must clear. Consider under-filling the
   OAP or shortening the tubes.
4. **Humidity from transpiration.** A closed loop over a transpiring leaf saturates
   quickly. Either accept and measure it (log RH, correct the response using the
   Stage A curve) or put a Nafion drier in the loop — but note a drier will also
   strip polar markers, so characterise its transmission first.

---

## 6. One-line answer

**Take closed-loop stripping (Tholl 2006, Fig. 3), delete the adsorbent trap, put the
ADM in the loop, and shrink the enclosure to the leaf-clamp micro-chamber geometry of
Li 2021 — then validate it against a push–pull open chamber (Tholl 2006, Fig. 4c) as
Tholl explicitly requires.**
