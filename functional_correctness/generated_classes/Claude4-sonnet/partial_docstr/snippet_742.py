class Material:
    '''
    A material meta class to rule them all.
    '''

    def __init__(self, label="Material", **kwargs):
        self.label = label
        self.properties = kwargs

    def get_template(self):
        template = f"*MATERIAL, NAME={self.label}\n"
        return template

    def write_inp(self):
        '''
        Returns the material definition as a string in Abaqus INP format.
        '''
        inp_string = self.get_template()
        
        for prop_name, prop_value in self.properties.items():
            if isinstance(prop_value, (list, tuple)):
                values = ", ".join(str(v) for v in prop_value)
                inp_string += f"*{prop_name.upper()}\n{values}\n"
            else:
                inp_string += f"*{prop_name.upper()}\n{prop_value}\n"
        
        return inp_string