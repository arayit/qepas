# Selection Framework — City-First Phase

**Revision 2, 1 September 2026.** Supersedes §0 of `_source-2026-09-01.md`.

---

## 0. Why the criteria list needed rebuilding

The previous version was a flat checklist: hard requirements, preferred, excluded.
It failed on its first hard case. Rauschenbeutel came out as *"very high calibre,
table-top, but atomic physics"* and was filed under **"high calibre, wrong axis"** —
a rejection — while simultaneously being the most impressive group in the Berlin
survey by every objective measure of scientific standing.

That contradiction is not a judgement call gone wrong. It is a structural fault in
the checklist. Three specific defects:

1. **Topic labels were treated as disqualifiers.** "Atomic physics", "quantum optics",
   "quantum materials" appear in the exclusion list. But the stated primary filter is
   *"the calibre of the science is the primary filter, not the topic."* The list
   contradicts its own first principle. A label on a webpage is not a property of the
   physics.

2. **"Develops its own source" was a proxy standing in for something else.** The thing
   actually wanted is: *the group builds the apparatus that makes the physics possible,
   rather than buying it.* For Picqué that apparatus is a comb. For Steinmeyer it is a
   mid-IR laser. For Rauschenbeutel it is a sub-wavelength tapered fibre and the trap
   geometry around it — pulled, characterised and engineered in-house, and the actual
   invention. The proxy rejects the third case; the real criterion accepts it.

3. **Hard gates and soft preferences were mixed into one list.** "No large facility" is
   a gate — fail it and nothing else matters. "Mid-IR adjacency" is a preference — it
   trades against calibre. Putting them in the same list makes every criterion feel
   equally binding and produces false rejections.

Revision 2 separates gates from axes, and replaces topic labels with the mechanism
underneath them.

---

## 1. Hard gates (binary; failing one ends the assessment)

A gate is something that, if violated, makes the PhD the wrong PhD regardless of how
good the group is.

| # | Gate | Test | Why it is a gate |
|---|---|---|---|
| G1 | **Experimental, table-top** | The apparatus fits in a lab the group controls | Non-negotiable working style |
| G2 | **No external large-facility dependence** | Can the central experiment run without booking beamtime at a synchrotron, FEL, or accelerator someone else owns? | Expertise must be portable; beamtime schedules dictate the thesis |
| G3 | **Not fabrication-dominated** | Is >50% of the student's time in a cleanroom? | Fabrication skill does not transfer to the intended career line |
| G4 | **Not software/simulation/reconstruction-dominated** | Is the intellectual product an algorithm? | Wanted: hardware physics |
| G5 | **The group builds its central apparatus** | Does the key instrument come out of a catalogue, or out of the lab? | This is the reformulation of "own source" — see §0.2 |
| G6 | **Europe, start Spring–Fall 2027** | — | Logistics |

Notes on applying the gates:

- **G2 is about ownership, not vacuum.** A UHV chamber on an optical table passes. A
  table-top HHG beamline in the group's own lab passes. Booking time at BESSY, PETRA,
  European XFEL, FERMI or LCLS fails. The previous list said "vacuum/beamline-heavy",
  which conflated the two and is why the ETH-Wörner rejection was recorded with a
  reason that does not generalise cleanly.
- **G5 is the load-bearing gate** and the one most often misapplied. It asks what the
  group *builds*, not what the group *builds it out of*. A group that pulls its own
  nanofibres and designs its own trap passes even if the diode lasers are bought. A
  group that buys a turnkey amplifier and does spectroscopy with it fails, even if the
  spectroscopy is excellent.

---

## 2. Soft axes (scored; these trade against each other)

Everything that survives the gates is scored on five axes, 0–5. Weights reflect the
stated priority order: calibre first, then what the thesis produces, then topic.

| Axis | Weight | 5 | 3 | 1 |
|---|---|---|---|---|
| **A. Calibre** — is this science at Ömer's level? Judged on where the work lands, what it changes, and whether the group sets a direction or follows one | ×3 | Founding-level; defines a subfield | Strong, competitive, derivative of a direction set elsewhere | Solid but incremental |
| **B. Deliverable type** — what does the thesis produce? | ×2 | A device, a technique, or device physics | A method others adopt | A measurement, or a better source someone else then uses |
| **C. Build content** — how much of the apparatus is the student's own | ×2 | The central instrument is invented and built in-group | Substantial in-house build on a bought platform | Assembly and alignment of bought parts |
| **D. Topic adjacency** — distance from the mid-IR / field-resolved / nonlinear-optics background | ×1 | Direct continuation | Same toolkit, different object | Genuine pivot; background does not transfer |
| **E. Group dynamics** — small, independently funded, hungry | ×1 | ERC-scale, young or newly independent, recruiting | Established, well-funded, stable | Large service group, or a PI near retirement |

**Weighting rationale.** A×3 encodes "calibre is the primary filter." B and C at ×2
encode the working-style requirements that actually distinguish this search from a
generic photonics search. D at ×1 is deliberate and is the main change from revision 1:
topic adjacency is a *convenience*, not a requirement, and it must not outweigh calibre.
A group scoring 5 on calibre and 1 on adjacency (15+1) beats a group scoring 3 and 5
(9+5). That is the intended behaviour.

Maximum is 45. The numbers are bookkeeping — they force the trade-offs to be stated
rather than felt, and they are not a measurement. Read the score alongside the note.

---

## 3. The topic-label problem, resolved

The following labels are **not** grounds for rejection on their own. Each is replaced
by the question that actually matters:

| Label | Question to ask instead |
|---|---|
| "Quantum optics" | Is the physics nonlinear/classical optics wearing a quantum label? (Ramelow: yes. Rauschenbeutel: no — but see G5) |
| "Atomic physics" | Is the atom the object of study, or the probe/resource in an engineered photonic system? |
| "Quantum materials" | Is the material the object, or the medium for a light–matter engineering problem? |
| "Metrology" | Comb/source development, or wafer and sample characterisation? Only the second is excluded |
| "Quantum computing hardware" | Still a hard exclusion — the engineering is qubit-count-driven, not physics-driven |

The one genuine remaining topic exclusion is **precision atomic/molecular metrology
aimed at fundamental-physics tests** (VU LaserLaB, Peters at HU). Reason: the physics
question is external to the apparatus, and the apparatus is in service of a number.
That is a real structural objection, not a label.

---

## 4. City layer

Cities are a **filter applied after** group assessment, not a competing score. The
practical version:

**City gates:** population large enough for anonymity; daily life workable in English;
non-car-dependent; a rental market where a self-contained one-bedroom with a cat is
actually obtainable on a PhD salary.

The last one is doing more work than it appears. It removes Amsterdam in practice even
though Amsterdam passes on paper, and it is the single strongest argument for the
Vienna and Rotterdam options.

**City tiers, from §3 of the source document:**

- **Tier 1 (gates pass comfortably):** Vienna, Berlin, Rotterdam, Brussels, Barcelona
- **Tier 2 (one gate strained):** Amsterdam (housing), Hamburg (rents), Paris (rent vs. pay, commute), Milan (pay)
- **Tier 3 (fails a gate):** Copenhagen, Stockholm (housing/queues), Munich, Zurich (cost, social closure)

**The named exception.** The city-first rule is suspended for a group scoring ≥38/45.
That threshold is set deliberately at the level Fattahi and Stiller reach in Erlangen.
A group that good is worth a town of 115,000. Below it, the city gate binds.

---

## 5. Working order

1. Apply gates G1–G6. Record which gate failed and why — the reason must generalise.
2. Score survivors on A–E.
3. Apply the city filter, with the ≥38 exception.
4. Verify time-sensitive facts (leadership, retirements, openings) before contacting anyone.

Step 4 is not a formality. This revision alone caught a retirement, an institute merger,
two departures and a chair vacancy that revision 1 had wrong or missing.
