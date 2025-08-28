class Cstatement_target:
    '''Represents the statement_target element'''

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
            self.node = ET.Element('statement_target')
            self.span = None
        else:
            self.node = node
            span_elem = self.node.find('span')
            if span_elem is not None:
                self.span = Cspan(span_elem, type)
            else:
                self.span = None

    def get_node(self):
        '''
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        '''
        return self.node

    def get_span(self):
        '''
        Returns the span of the statement_target element
        @rtype: L{Cspan}
        @return: span object
        '''
        return self.span

    def set_span(self, my_span):
        '''
        Sets the id of the element
        @type my_span: L{Cspan}
        @param my_span: the span of the statement_target
        '''
        # Remove existing span if any
        for existing in self.node.findall('span'):
            self.node.remove(existing)
        # Attach new span
        self.node.append(my_span.get_node())
        self.span = my_span