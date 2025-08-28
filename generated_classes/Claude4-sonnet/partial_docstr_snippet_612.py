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
        pattern = r'\bout\s+\w+\s+(\w+)\s*;'
        matches = re.findall(pattern, self.source)
        return matches

    def print(self):
        '''Print the shader lines'''
        lines = self.source.split('\n')
        for i, line in enumerate(lines, 1):
            print(f"{i:3d}: {line}")