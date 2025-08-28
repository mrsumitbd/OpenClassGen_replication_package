class SubObjectTree(object):
    def __init__(self, items, item_paths):
        self.items = items
        self.item_paths = item_paths

    def copy(self):
        return SubObjectTree(self.items.copy(), self.item_paths.copy())

    def __iter__(self):
        return iter(self.items)

    def __str__(self):
        return f"SubObjectTree(items={self.items}, item_paths={self.item_paths})"