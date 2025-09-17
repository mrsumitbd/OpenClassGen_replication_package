class MapColumns(object):
    '''
    directly maps columns in tables to aikif structures
    '''

    def __init__(self, col_file):
        '''
        takes a raw row in the map file and extracts info
        '''
        self.col_file = col_file
        self.rules = []
        self.load_rules()

    def __str__(self):
        return f"MapColumns with {len(self.rules)} rules from {self.col_file}"

    def load_rules(self):
        ''' 
        load the rules from file
        '''
        try:
            with open(self.col_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        self.rules.append(line)
        except FileNotFoundError:
            self.rules = []