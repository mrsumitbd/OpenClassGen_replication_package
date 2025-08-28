class ColumnHeader(object):

    def __init__(self, text=None, attrs=None, row_order=0):
        self._text = text
        self._attrs = attrs or {}
        self._row_order = row_order

    @property
    def attrs(self):
        return self._attrs