"""Skeletal structures: n-hexyl acetate (NIST gas-phase proxy) vs (Z)-3-hexenyl acetate (target).

Blue = acetate group shared by both (source of the ~1235 cm^-1 C-O band).
Orange = the cis C=C bond, the only difference.
Run: python figures/hexenyl_acetate_structures.py
"""
from pathlib import Path
from rdkit import Chem
from rdkit.Chem import AllChem, rdDepictor
from rdkit.Chem.Draw import rdMolDraw2D

OUT = Path(__file__).with_name("hexenyl_acetate_structures")
BLUE = (0.165, 0.471, 0.839, 0.35)
ORANGE = (0.922, 0.408, 0.204, 0.55)

mols = [
    ("CCCCCCOC(C)=O", "n-Hexyl acetate (proxy, NIST gas IR)\nC8H16O2   CAS 142-92-7"),
    ("CC/C=C\\CCOC(C)=O", "(Z)-3-Hexenyl acetate (target, GLV)\nC8H14O2   CAS 3681-71-8"),
]
acetate = Chem.MolFromSmarts("[CH3]C(=O)O")
alkene = Chem.MolFromSmarts("C=C")

ms, legends, hl_atoms, hl_bonds, atom_cols, bond_cols = [], [], [], [], [], []
for smi, leg in mols:
    m = Chem.MolFromSmiles(smi)
    if not ms:
        AllChem.Compute2DCoords(m)
    else:  # same atom order in both SMILES: align ester end + CH2CH2 to the proxy
        rdDepictor.GenerateDepictionMatching2DStructure(m, ms[0], atomMap=[(i, i) for i in range(4, 10)])
    a_idx, b_idx, ac, bc = [], [], {}, {}
    for match in m.GetSubstructMatches(acetate):
        for i in match:
            a_idx.append(i); ac[i] = BLUE
        for b in m.GetBonds():
            if b.GetBeginAtomIdx() in match and b.GetEndAtomIdx() in match:
                b_idx.append(b.GetIdx()); bc[b.GetIdx()] = BLUE
    for match in m.GetSubstructMatches(alkene):
        for i in match:
            a_idx.append(i); ac[i] = ORANGE
        b = m.GetBondBetweenAtoms(*match)
        b_idx.append(b.GetIdx()); bc[b.GetIdx()] = ORANGE
    ms.append(m); legends.append(leg)
    hl_atoms.append(a_idx); hl_bonds.append(b_idx); atom_cols.append(ac); bond_cols.append(bc)

for ext in ("png", "svg"):
    d = (rdMolDraw2D.MolDraw2DCairo(1000, 380, 500, 380) if ext == "png"
         else rdMolDraw2D.MolDraw2DSVG(1000, 380, 500, 380))
    o = d.drawOptions()
    o.legendFontSize = 22
    o.bondLineWidth = 2
    o.fixedBondLength = 45
    o.setBackgroundColour((1, 1, 1, 1))
    d.DrawMolecules(ms, legends=legends, highlightAtoms=hl_atoms, highlightBonds=hl_bonds,
                    highlightAtomColors=atom_cols, highlightBondColors=bond_cols)
    d.FinishDrawing()
    data = d.GetDrawingText()
    (OUT.with_suffix("." + ext)).write_bytes(data if isinstance(data, bytes) else data.encode())
print("wrote", OUT)
