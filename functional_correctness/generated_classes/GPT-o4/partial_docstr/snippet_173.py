class ToExpand(object):
    def __init__(self, s, indexes=None):
        self.s = s
        if indexes is None:
            self.indexes = self.find_indexes()
        else:
            self.indexes = indexes

    def find_indexes(self):
        s = self.s
        level = 0
        start = None
        for i, ch in enumerate(s):
            if ch == '(':
                if level == 0:
                    start = i
                level += 1
            elif ch == ')':
                level -= 1
                if level == 0 and start is not None:
                    content = s[start+1:i]
                    # check for a top‐level '|'
                    lvl = 0
                    for c in content:
                        if c == '(':
                            lvl += 1
                        elif c == ')':
                            lvl -= 1
                        elif c == '|' and lvl == 0:
                            return (start, i)
                    return None
        return None

    def expand_one(self):
        if self.indexes is None:
            return []
        start, end = self.indexes
        content = self.s[start+1:end]
        parts = []
        last = 0
        lvl = 0
        for i, ch in enumerate(content):
            if ch == '(':
                lvl += 1
            elif ch == ')':
                lvl -= 1
            elif ch == '|' and lvl == 0:
                parts.append(content[last:i])
                last = i + 1
        parts.append(content[last:])
        results = []
        for part in parts:
            new_s = self.s[:start] + part + self.s[end+1:]
            results.append(ToExpand(new_s))
        return results

    def fully_expanded(self):
        return self.indexes is None

    def __repr__(self):
        return f"ToExpand({self.s!r})"