class Material:
    '''
    A material meta class to rule them all.
    '''

    def __init__(self, label="Material", **kwargs):
        self.label = label
        self.properties = {}
        for key, value in kwargs.items():
            # normalize property values to tuples
            if isinstance(value, (int, float)):
                vals = (value,)
            elif isinstance(value, (list, tuple)):
                vals = tuple(value)
            else:
                raise TypeError(f"Unsupported type for property '{key}': {type(value)}")
            self.properties[key] = vals

    def get_template(self):
        lines = [f"*Material, name={self.label}"]
        for key, vals in self.properties.items():
            k = key.lstrip("*")
            lines.append(f"*{k}")
            lines.append(", ".join(str(v) for v in vals))
        return "\n".join(lines)

    def write_inp(self):
        '''
        Returns the material definition as a string in Abaqus INP format.
        '''
        return self.get_template()