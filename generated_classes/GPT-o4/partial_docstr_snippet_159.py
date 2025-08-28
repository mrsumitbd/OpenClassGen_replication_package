class Frame:
    '''A content iterator frame.'''

    def __init__(self, sx):
        '''
        @param sx: A schema object.
        @type sx: L{SchemaObject}
        '''
        self._iterator = iter(sx)

    def next(self):
        '''
        Get the I{next} item in the frame's collection.

        @return: The next item or None
        @rtype: L{SchemaObject}
        '''
        try:
            return next(self._iterator)
        except StopIteration:
            return None