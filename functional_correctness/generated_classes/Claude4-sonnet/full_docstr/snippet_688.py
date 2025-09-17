class AttrList:
    '''
    A filtered attribute list.
    Items are included during iteration if they are in either the (xs) or
    (xml) namespaces.
    @ivar raw: The I{raw} attribute list.
    @type raw: list
    '''

    def __init__(self, attributes):
        '''
        @param attributes: A list of attributes
        @type attributes: list
        '''
        self.raw = attributes

    def real(self):
        '''
        Get list of I{real} attributes which exclude xs and xml attributes.
        @return: A list of I{real} attributes.
        @rtype: I{generator}
        '''
        for attr in self.raw:
            if not self.skip(attr):
                yield attr

    def rlen(self):
        '''
        Get the number of I{real} attributes which exclude xs and xml attributes.
        @return: A count of I{real} attributes. 
        @rtype: L{int}
        '''
        return len(list(self.real()))

    def lang(self):
        '''
        Get list of I{filtered} attributes which exclude xs.
        @return: A list of I{filtered} attributes.
        @rtype: I{generator}
        '''
        for attr in self.raw:
            if hasattr(attr, 'namespace') and attr.namespace != 'xs':
                yield attr
            elif not hasattr(attr, 'namespace'):
                yield attr

    def skip(self, attr):
        '''
        Get whether to skip (filter-out) the specified attribute.
        @param attr: An attribute.
        @type attr: I{Attribute}
        @return: True if should be skipped.
        @rtype: bool
        '''
        if hasattr(attr, 'namespace'):
            return attr.namespace in ('xs', 'xml')
        return False