class Frame:
    '''A content iterator frame.'''

    def __init__(self, sx):
        '''
        @param sx: A schema object.
        @type sx: L{SchemaObject}
        '''
        self.sx = sx
        self.items = []
        self.index = 0
        
        # If sx has children or items, populate the frame
        if hasattr(sx, 'children') and sx.children:
            self.items = list(sx.children)
        elif hasattr(sx, 'items') and sx.items:
            self.items = list(sx.items)
        elif hasattr(sx, '__iter__'):
            try:
                self.items = list(sx)
            except:
                self.items = []

    def next(self):
        '''
        Get the I{next} item in the frame's collection.

        @return: The next item or None
        @rtype: L{SchemaObject}
        '''
        if self.index < len(self.items):
            item = self.items[self.index]
            self.index += 1
            return item
        return None