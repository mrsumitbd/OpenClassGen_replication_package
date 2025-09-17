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
        self.mappings = {}
        if col_file:
            self.load_rules()

    def __str__(self):
        result = f"MapColumns: {self.col_file}\n"
        result += f"Number of rules: {len(self.rules)}\n"
        for rule in self.rules:
            result += f"  {rule}\n"
        return result

    def load_rules(self):
        ''' 
        load the rules from file
        '''
        try:
            with open(self.col_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split(',')
                        if len(parts) >= 2:
                            source_col = parts[0].strip()
                            target_col = parts[1].strip()
                            rule = {
                                'source': source_col,
                                'target': target_col,
                                'line_num': line_num
                            }
                            if len(parts) > 2:
                                rule['transform'] = parts[2].strip()
                            self.rules.append(rule)
                            self.mappings[source_col] = target_col
        except FileNotFoundError:
            self.rules = []
            self.mappings = {}
        except Exception as e:
            self.rules = []
            self.mappings = {}