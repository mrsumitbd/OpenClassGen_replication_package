class Material:
    '''
    A material meta class to rule them all.
    '''

    def __init__(self, label="Material", **kwargs):
        self.label = label
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_template(self):
        return f"*MATERIAL, NAME={self.label}\n"

    def write_inp(self):
        '''
        Returns the material definition as a string in Abaqus INP format.
        '''
        return self.get_template()