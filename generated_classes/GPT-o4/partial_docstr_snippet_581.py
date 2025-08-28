class MetalDisconnector(object):
    '''Class for breaking covalent bonds between metals and organic atoms under certain conditions.'''

    def __init__(self):
        # Transition metals + Al
        transitions = ['Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn',
                       'Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd',
                       'Hf','Ta','W','Re','Os','Ir','Pt','Au']
        metals = set(transitions + ['Al'])
        # Excluded metals
        exclude = {'Hg','Ga','Ge','In','Sn','As','Tl','Pb','Bi','Po'}
        self.metals = metals - exclude
        # Atoms always disconnected from any metal
        self.always_detach = {'N','O','F'}
        # Other non-metals to detach from selected metals
        self.other_detach = {'P','S','Cl','Br','I'}
        # Define organic non-metals
        self.org_nonmetals = {'H','C','N','O','F','P','S','Cl','Br','I'}

    def __call__(self, mol):
        return self.disconnect(mol)

    def disconnect(self, mol):
        rw = Chem.RWMol(mol)
        to_remove = []
        charge_updates = {}
        for bond in mol.GetBonds():
            i = bond.GetBeginAtomIdx()
            j = bond.GetEndAtomIdx()
            a1 = mol.GetAtomWithIdx(i)
            a2 = mol.GetAtomWithIdx(j)
            s1 = a1.GetSymbol()
            s2 = a2.GetSymbol()
            pair = None
            # always detach N, O, F from any metal
            if s1 in self.always_detach and s2 not in self.org_nonmetals:
                pair = (j, i)
            elif s2 in self.always_detach and s1 not in self.org_nonmetals:
                pair = (i, j)
            # detach other non-metals from selected metals
            elif s1 in self.other_detach and s2 in self.metals:
                pair = (j, i)
            elif s2 in self.other_detach and s1 in self.metals:
                pair = (i, j)
            if pair:
                metal_idx, org_idx = pair
                to_remove.append((metal_idx, org_idx))
                # adjust charges: metal +1, organic -1
                metal_fc = rw.GetAtomWithIdx(metal_idx).GetFormalCharge()
                org_fc = rw.GetAtomWithIdx(org_idx).GetFormalCharge()
                charge_updates[metal_idx] = metal_fc + 1
                charge_updates[org_idx] = org_fc - 1
        # remove bonds and update charges
        for m, o in to_remove:
            try:
                rw.RemoveBond(m, o)
            except:
                pass
        for idx, new_fc in charge_updates.items():
            rw.GetAtomWithIdx(idx).SetFormalCharge(new_fc)
        # sanitize and return
        rdmolops.SanitizeMol(rw)
        return rw.GetMol()