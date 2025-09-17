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
        lines = []
        for r in self.rules:
            lines.append(f"{r['table']}.{r['column']} -> {r['structure']}.{r['field']}")
        return "\n".join(lines)

    def load_rules(self):
        ''' 
        load the rules from file
        '''
        with open(self.col_file, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                first = row[0].strip()
                if first.startswith('#') or first == '':
                    continue
                if len(row) < 4:
                    raise ValueError(f"Invalid mapping row: {row}")
                table, column, structure, field = (cell.strip() for cell in row[:4])
                self.rules.append({
                    'table': table,
                    'column': column,
                    'structure': structure,
                    'field': field
                })