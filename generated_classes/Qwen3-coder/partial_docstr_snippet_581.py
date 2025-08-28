class MetalDisconnector(object):
    '''Class for breaking covalent bonds between metals and organic atoms under certain conditions.'''

    def __init__(self):
        pass

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
        from rdkit import Chem
        import copy

        # Create a copy of the molecule to avoid modifying the original
        mol = copy.deepcopy(mol)
        Chem.SanitizeMol(mol)
        
        # Define element symbols
        disconnect_elements = {'N', 'O', 'F'}
        
        # Transition metals + Al
        transition_metals_plus_al = {
            13,  # Al
            21, 22, 23, 24, 25, 26, 27, 28, 29, 30,  # Sc to Zn
            39, 40, 41, 42, 43, 44, 45, 46, 47, 48,  # Y to Cd
            57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71,  # La to Lu
            72, 73, 74, 75, 76, 77, 78, 79, 80  # Hf to Hg
        }
        
        # Excluded elements
        excluded_elements = {'Hg', 'Ga', 'Ge', 'In', 'Sn', 'As', 'Tl', 'Pb', 'Bi', 'Po'}
        excluded_atomic_nums = {Chem.AtomFromSmiles(elem).GetAtomicNum() for elem in excluded_elements}
        
        # Get atoms to disconnect from
        atoms_to_disconnect_from = set()
        for atom in mol.GetAtoms():
            atomic_num = atom.GetAtomicNum()
            symbol = atom.GetSymbol()
            
            # Check if it's a metal
            if atomic_num in transition_metals_plus_al and atomic_num not in excluded_atomic_nums:
                atoms_to_disconnect_from.add(atom.GetIdx())
            # Check if it's Al
            elif symbol == 'Al':
                atoms_to_disconnect_from.add(atom.GetIdx())
        
        # Store bonds to be broken
        bonds_to_break = []
        
        # Iterate through bonds
        for bond in mol.GetBonds():
            begin_atom = bond.GetBeginAtom()
            end_atom = bond.GetEndAtom()
            begin_idx = begin_atom.GetIdx()
            end_idx = end_atom.GetIdx()
            
            begin_symbol = begin_atom.GetSymbol()
            end_symbol = end_atom.GetSymbol()
            begin_atomic_num = begin_atom.GetAtomicNum()
            end_atomic_num = end_atom.GetAtomicNum()
            
            # Check if bond is between metal and organic atom
            begin_is_metal = begin_idx in atoms_to_disconnect_from or begin_symbol in ['Al']
            end_is_metal = end_idx in atoms_to_disconnect_from or end_symbol in ['Al']
            
            begin_is_organic = begin_symbol in disconnect_elements or (begin_atomic_num not in transition_metals_plus_al and begin_symbol not in excluded_elements and begin_symbol not in ['Al', 'C', 'H'])
            end_is_organic = end_symbol in disconnect_elements or (end_atomic_num not in transition_metals_plus_al and end_symbol not in excluded_elements and end_symbol not in ['Al', 'C', 'H'])
            
            # Case 1: Disconnect N, O, F from any metal
            if (begin_symbol in disconnect_elements and end_is_metal) or (end_symbol in disconnect_elements and begin_is_metal):
                bonds_to_break.append((begin_idx, end_idx))
            
            # Case 2: Disconnect other non-metals from transition metals + Al (but not excluded elements)
            elif begin_is_metal and end_is_organic and end_symbol not in disconnect_elements:
                bonds_to_break.append((begin_idx, end_idx))
            elif end_is_metal and begin_is_organic and begin_symbol not in disconnect_elements:
                bonds_to_break.append((begin_idx, end_idx))
        
        # Break bonds in reverse order to maintain indices
        for begin_idx, end_idx in reversed(bonds_to_break):
            mol.RemoveBond(begin_idx, end_idx)
            
            # Adjust charges
            begin_atom = mol.GetAtomWithIdx(begin_idx)
            end_atom = mol.GetAtomWithIdx(end_idx)
            
            # Metal loses electron (becomes more positive)
            if begin_atom.GetSymbol() in ['Al'] or begin_atom.GetAtomicNum() in transition_metals_plus_al:
                begin_atom.SetFormalCharge(begin_atom.GetFormalCharge() + 1)
                end_atom.SetFormalCharge(end_atom.GetFormalCharge() - 1)
            elif end_atom.GetSymbol() in ['Al'] or end_atom.GetAtomicNum() in transition_metals_plus_al:
                end_atom.SetFormalCharge(end_atom.GetFormalCharge() + 1)
                begin_atom.SetFormalCharge(begin_atom.GetFormalCharge() - 1)
        
        # Clear computed properties and sanitize
        mol.UpdatePropertyCache()
        
        return mol