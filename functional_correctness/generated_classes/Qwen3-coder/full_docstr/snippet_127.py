class VKeyRow(object):
    '''A VKeyRow defines a keyboard row which is composed of a list of
    VKey.

    This class aims to be created internally after parsing a keyboard
    layout model. It is used to optimize collision detection, by first
    checking row collision, then internal row key detection.
    '''

    def __init__(self):
        '''Default row constructor. '''
        self.keys = []
        self.position = None
        self.size = None
        self.padding = None

    def add_key(self, key, first=False):
        '''Adds the given key to this row.

        Parameters
        ----------
        key:
            Key to be added to this row.
        first:
            Flag that indicates if key is added at the beginning or at the end.
        '''
        if first:
            self.keys.insert(0, key)
        else:
            self.keys.append(key)

    def set_size(self, position, size, padding):
        '''Row size setter. The size correspond to the row height, since the
        row width is constraint to the surface width the associated keyboard
        belongs. Once size is settled, the size for each child keys is
        associated.

        Parameters
        ----------
        position:
            Position of this row.
        size:
            Size of the row (height)
        padding:
            Padding between key.
        '''
        self.position = position
        self.size = size
        self.padding = padding

    def __len__(self):
        '''len() operator overload.

        Returns
        -------
        len:
            Number of keys this row contains.
        '''
        return len(self.keys)