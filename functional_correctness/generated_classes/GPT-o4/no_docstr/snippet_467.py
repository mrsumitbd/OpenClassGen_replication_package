class SubObjectTree(object):
    def __init__(self, items, item_paths):
        self.items = []
        self.children = {}
        buckets = {}
        for item, path in zip(items, item_paths):
            if not path:
                self.items.append(item)
            else:
                key = path[0]
                rest = path[1:]
                if key not in buckets:
                    buckets[key] = ([], [])
                buckets[key][0].append(item)
                buckets[key][1].append(rest)
        for key, (sub_items, sub_paths) in buckets.items():
            self.children[key] = SubObjectTree(sub_items, sub_paths)

    def copy(self):
        new = SubObjectTree([], [])
        new.items = list(self.items)
        new.children = {k: v.copy() for k, v in self.children.items()}
        return new

    def __iter__(self):
        for key, subtree in self.children.items():
            yield key, subtree

    def __str__(self):
        lines = []
        def _rec(tree, indent):
            for it in tree.items:
                lines.append(" " * indent + repr(it))
            for key, sub in tree.children.items():
                lines.append(" " * indent + str(key))
                _rec(sub, indent + 2)
        _rec(self, 0)
        return "\n".join(lines)