class ShaderSource:
    '''
    Helper class representing a single shader type
    '''

    def __init__(self, shader_type: str, name: str, source: str):
        self.shader_type = shader_type
        self.name = name
        self.source = source
        self.lines = source.split('\n')

    def find_out_attribs(self):
        '''
        Get all out attributes in the shader source.

        :return: List of attribute names
        '''
        out_attribs = []
        out_pattern = r'\bout\s+\w+\s+(\w+)'
        
        for line in self.lines:
            matches = re.findall(out_pattern, line)
            out_attribs.extend(matches)
        
        return out_attribs

    def print(self):
        '''Print the shader lines'''
        for i, line in enumerate(self.lines, 1):
            print(f"{i:3}: {line}")