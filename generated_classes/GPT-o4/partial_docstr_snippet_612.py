class ShaderSource:
    '''
    Helper class representing a single shader type
    '''

    def __init__(self, shader_type: str, name: str, source: str):
        self.shader_type = shader_type
        self.name = name
        self.source = source

    def find_out_attribs(self):
        '''
        Get all out attributes in the shader source.

        :return: List of attribute names
        '''
        attrs = []
        for line in self.source.splitlines():
            code = line.split('//', 1)[0]
            match = re.match(r'\s*out\b(?:\s+\w+)*\s+([^;]+);', code)
            if match:
                names = match.group(1)
                for part in names.split(','):
                    name = part.strip().split()[0]
                    # strip array syntax if present
                    name = re.match(r'(\w+)', name).group(1)
                    attrs.append(name)
        return attrs

    def print(self):
        '''Print the shader lines'''
        for line in self.source.splitlines():
            print(line)