class ColumnHeader(object):

    def __init__(self, text=None, attrs=None, row_order=0):
        self.text = text
        self._attrs = {} if attrs is None else dict(attrs)
        self.row_order = row_order

    @property
    def attrs(self):
        return self._attrs