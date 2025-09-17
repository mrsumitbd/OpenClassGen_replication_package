class MetalDisconnector(object):
    '''Class for breaking covalent bonds between metals and organic atoms under certain conditions.'''

    def __init__(self):
        # Define sets of atomic numbers for different categories
        self.metals = {3, 4, 11, 12, 13, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118}
        self.transition_metals_and_al = {13, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112}
        self.excluded_metals = {80, 31, 32, 49, 50, 33, 81, 82, 83, 84}  # Hg, Ga, Ge, In, Sn, As, Tl, Pb, Bi, Po
        self.nof = {7, 8, 9}  # N, O, F

    def __call__(self, mol):
        '''Calling a MetalDisconnector instance like a function is the same as calling its disconnect(mol) method.'''
        return self.disconnect(mol)

    def disconnect(self, mol):
        '''Break covalent bonds between metals and organic atoms under certain conditions.

        The algorithm works as follows:

        - Disconnect N, O, F from any metal.
        - Disconnect other non-metals from transition metals + Al (but not Hg, Ga, Ge, In, Sn, As, Tl, Pb, Bi, Po).
        - For every bond broken, adjust the charges of the begin and end atoms accordingly.

        :param mol: The input molecule.
        :type mol: rdkit.Chem.rdchem.Mol
        :return: The molecule with metals disconnected.
        :rtype: rdkit.Chem.rdchem.Mol
        '''
        if mol is None:
            return None
            
        mol = Chem.Mol(mol)
        
        # Get editable molecule
        em = Chem.EditableMol(mol)
        
        # Find bonds to remove
        bonds_to_remove = []
        
        for bond in mol.GetBonds():
            begin_atom = bond.GetBeginAtom()
            end_atom = bond.GetEndAtom()
            begin_atomic_num = begin_atom.GetAtomicNum()
            end_atomic_num = end_atom.GetAtomicNum()
            
            # Check if one atom is metal and one is non-metal
            begin_is_metal = begin_atomic_num in self.metals
            end_is_metal = end_atomic_num in self.metals
            
            if begin_is_metal and not end_is_metal:
                metal_atom = begin_atom
                nonmetal_atom = end_atom
                metal_atomic_num = begin_atomic_num
                nonmetal_atomic_num = end_atomic_num
            elif end_is_metal and not begin_is_metal:
                metal_atom = end_atom
                nonmetal_atom = begin_atom
                metal_atomic_num = end_atomic_num
                nonmetal_atomic_num = begin_atomic_num
            else:
                continue
                
            should_disconnect = False
            
            # Rule 1: Disconnect N, O, F from any metal
            if nonmetal_atomic_num in self.nof:
                should_disconnect = True
            
            # Rule 2: Disconnect other non-metals from transition metals + Al (but not excluded metals)
            elif (metal_atomic_num in self.transition_metals_and_al and 
                  metal_atomic_num not in self.excluded_metals):
                should_disconnect = True
                
            if should_disconnect:
                bonds_to_remove.append((bond.GetIdx(), metal_atom.GetIdx(), nonmetal_atom.GetIdx()))
        
        # Remove bonds in reverse order to maintain indices
        bonds_to_remove.sort(reverse=True)
        
        for bond_idx, metal_idx, nonmetal_idx in bonds_to_remove:
            # Adjust charges before removing bond
            metal_atom = mol.GetAtomWithIdx(metal_idx)
            nonmetal_atom = mol.GetAtomWithIdx(nonmetal_idx)
            
            # Get current charges
            metal_charge = metal_atom.GetFormalCharge()
            nonmetal_charge = nonmetal_atom.GetFormalCharge()
            
            # Adjust charges based on bond order
            bond = mol.GetBondWithIdx(bond_idx)
            bond_order = int(bond.GetBondType())
            
            # Metal loses electrons (becomes more positive)
            # Non-metal gains electrons (becomes more negative)
            metal_atom.SetFormalCharge(metal_charge + bond_order)
            nonmetal_atom.SetFormalCharge(nonmetal_charge - bond_order)
            
            # Remove the bond
            em.RemoveBond(metal_idx, nonmetal_idx)
        
        # Get the modified molecule
        result_mol = em.GetMol()
        
        if result_mol is not None:
            try:
                Chem.SanitizeMol(result_mol)
            except:
                # If sanitization fails, return the molecule without sanitization
                pass
                
        return result_mol