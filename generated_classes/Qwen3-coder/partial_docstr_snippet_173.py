class ToExpand(object):
    def __init__(self, s, indexes=None):
        self.s = s
        if indexes is None:
            self.indexes = self.find_indexes()
        else:
            self.indexes = indexes

    def find_indexes(self):
        indexes = []
        stack = []
        for i, char in enumerate(self.s):
            if char == '[':
                stack.append(i)
            elif char == ']':
                if stack:
                    start = stack.pop()
                    indexes.append((start, i))
        return indexes

    def expand_one(self):
        '''expand the more-to-the-left/outer bracket, return a list of ToExpand's'''
        if not self.indexes:
            return []
        
        # Find the outermost bracket (leftmost opening bracket)
        outermost = min(self.indexes, key=lambda x: x[0])
        start, end = outermost
        
        # Get the part before the bracket, inside the bracket, and after the bracket
        before = self.s[:start]
        inside = self.s[start+1:end]
        after = self.s[end+1:]
        
        # Split the inside content by comma
        parts = [part.strip() for part in inside.split(',')]
        
        # Create new ToExpand objects for each possibility
        result = []
        for part in parts:
            new_s = before + part + after
            # Recalculate indexes for the new string
            new_obj = ToExpand(new_s)
            result.append(new_obj)
        
        return result

    def fully_expanded(self):
        return len(self.indexes) == 0

    def __repr__(self):
        return f"ToExpand('{self.s}', {self.indexes})"