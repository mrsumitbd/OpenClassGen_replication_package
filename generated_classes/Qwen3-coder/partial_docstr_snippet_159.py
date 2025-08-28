class Frame:
    '''A content iterator frame.'''


    def __init__(self, sx):
        '''
        @param sx: A schema object.
        @type sx: L{SchemaObject}

        '''
        self.sx = sx
        self.index = 0
        self.collection = getattr(sx, 'content', [])


    def next(self):
        '''
        Get the I{next} item in the frame's collection.

        @return: The next item or None
        @rtype: L{SchemaObject}

        '''
        if self.index < len(self.collection):
            item = self.collection[self.index]
            self.index += 1
            return item
        return None