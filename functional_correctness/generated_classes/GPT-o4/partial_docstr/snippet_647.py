class Ame2003(object):
    '''An interface to a subset of the data from Ame2003.

       This object contains an attribute masses. This is a dictionary whose keys
       are the proton numbers (Z) and values are the corresponding values are
       again dictionaries. The latter dictionaries have the mass number (A) as
       keys and the corresponding isotope masses in atomic units as values. E.g.
       self.masses[6][12] is the mass of carbon 12.

       If you use this interface, cite the following references:

       The AME2003 atomic mass evaluation (I). Evaluation of input data, adjustment
       procedures. A.H. Wapstra, G. Audi, and C. Thibault. Nuclear Physics A729,
       129 (2003).

       The AME2003 atomic mass evaluation (II). Tables, graphs, and references. G.
       Audi, A.H. Wapstra, and C. Thibault. Nuclear Physics A729, 337 (2003).
    '''
    def __init__(self):
        '''
           An object of this type is created in this module, so there is not
           need to construct it manually.
        '''
        self.masses = {}

    def add_mass(self, N, Z, mass):
        '''Put a new mass into the dictionary'''
        A = N + Z
        if Z not in self.masses:
            self.masses[Z] = {}
        self.masses[Z][A] = mass