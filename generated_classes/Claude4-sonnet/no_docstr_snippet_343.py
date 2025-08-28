class Algorithm:
    def __init__(self):
        self.name = "Base Algorithm"
        self.version = "1.0"
        self.parameters = {}
    
    def generate(self, cli_object):
        if cli_object is None:
            return None
        
        result = {
            'algorithm': self.name,
            'version': self.version,
            'input': str(cli_object),
            'output': self._process(cli_object),
            'parameters': self.parameters.copy()
        }
        
        return result
    
    def _process(self, cli_object):
        return f"Processed: {cli_object}"
    
    def set_parameter(self, key, value):
        self.parameters[key] = value
    
    def get_parameter(self, key, default=None):
        return self.parameters.get(key, default)