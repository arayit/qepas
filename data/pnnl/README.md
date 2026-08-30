# data/pnnl — candidate VOC spectra

Drop one CSV per compound here, named `<compound>.csv`, then run:

    python3 analysis/voc_band_ranking.py \
        --pnnl data/pnnl \
        --par  ../thesis/data/hitran/h2o_n2o_1111-2000_hitran.par

## Format

Two columns, `wavenumber_cm-1, absorbance`. Header row optional; comma or
whitespace separated; comment lines starting with `#` are ignored. The loader
sorts by wavenumber, so ascending or descending both work.

Absorbance must be in the **PNNL/NWIR convention**: base-10 absorbance
normalised to a burden of 1 ppm·m at 1 atm and 296 K. The script converts with

    sigma [cm^2/molecule] = 9.287e-16 * A_PNNL

If a spectrum comes from somewhere else, note the normalisation in a `#`
comment at the top of the file — the conversion factor is the one thing that
cannot be recovered from the numbers alone.

## Priority compounds

| Compound | CAS | Why |
|---|---|---|
| (Z)-3-hexenyl acetate | 3681-71-8 | GLV ester from cut grass; acetate C–O ~1240 |
| Methyl salicylate | 119-36-8 | Systemic disease signal; aryl ester |
| Ethyl acetate | 141-78-6 | Step 1 test compound; same acetate band |
| Hexanal | 66-25-1 | GLV aldehyde; C=O ~1730, deep in the water band |
| (E)-2-hexenal | 6728-26-3 | Stable hexenal isomer |
| Methyl jasmonate | 39924-52-2 | Wound hormone |
| Indole | 120-72-9 | Maize herbivory marker |
| 4-ethylphenol | 123-07-9 | Crown rot marker (Li 2019) |
| Eugenol | 97-53-0 | Aromatic, strong aryl–O |

Verify CAS numbers before ordering anything.

## Sources

- **NIST Chemistry WebBook** — free, no registration, gas-phase IR.
  `webbook.nist.gov/cgi/cbook.cgi?ID=C<cas-digits>&Type=IR-SPEC`
  Good for band positions; not quantitative in the PNNL sense.
- **PNNL / NWIR** — the quantitative library, ~500 species, 0.1 cm⁻¹,
  pressure-broadened to 1 atm in N₂ at 296 K. Cite Sharpe et al. (2004),
  *Appl. Spectrosc.* **58**(12), 1452–1461.
- **DTIC ADA392033** — quantitative vapour-phase FTIR measured with a
  saturator cell and 10 m gas cell at 30 °C; covers methyl salicylate.
