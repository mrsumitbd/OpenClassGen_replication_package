class ToExpand (object):

    def __init__ (self, s, indexes=None):
        self.s = s
        self.indexes = indexes if indexes is not None else self.find_indexes()

    def find_indexes (self):
        indexes = []
        depth = 0
        start = -1
        
        for i, char in enumerate(self.s):
            if char == '{':
                if depth == 0:
                    start = i
                depth += 1
            elif char == '}':
                depth -= 1
                if depth == 0 and start != -1:
                    indexes.append((start, i))
                    start = -1
        
        return indexes

    def expand_one (self):
        '''expand the more-to-the-left/outer bracket, return a list of ToExpand's'''
        if not self.indexes:
            return [self]
        
        start, end = self.indexes[0]
        bracket_content = self.s[start+1:end]
        options = bracket_content.split(',')
        
        result = []
        for option in options:
            new_s = self.s[:start] + option + self.s[end+1:]
            result.append(ToExpand(new_s))
        
        return result

    def fully_expanded (self):
        return len(self.indexes) == 0

    def __repr__ (self):
        return self.s