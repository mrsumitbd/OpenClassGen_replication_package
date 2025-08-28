class Cproperties:
    '''
    This class encapsulates the property layer in KAF/NAF
    '''

    def __init__(self, node=None, type='NAF'):
        '''
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        @type type: string
        @param type: the type of the object (KAF or NAF)
        '''
        self.type = type
        if node is None:
            self.node = Element('properties')
        else:
            self.node = node

    def get_node(self):
        '''
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        '''
        return self.node

    def __iter__(self):
        '''
        Iterator that returns all the properties
        @rtype: L{Cproperty}
        @return: list of properties (iterator)
        '''
        for prop in self.node.findall('property'):
            yield Cproperty(prop, self.type)

    def add_property(self, pid, label, term_span):
        '''
        Adds a new property to the property layer
        @type pid: string
        @param pid: property identifier
        @type label: string
        @param label: the label of the property
        @type term_span: list
        @param term_span: list of term identifiers
        '''
        prop_el = SubElement(self.node, 'property', {'pid': pid, 'label': label})
        span_el = SubElement(prop_el, 'span')
        for tid in term_span:
            SubElement(span_el, 'target', {'id': tid})
        return Cproperty(prop_el, self.type)