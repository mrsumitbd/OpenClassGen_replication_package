class Cstatement_source:
    '''Represents the statement_source element'''
    def __init__(self, node=None, type='NAF'):
        '''
        Constructor of the object
        @type node: xml Element or None (to create and empty one)
        @param node:  this is the node of the element. If it is None it will create a new object
        @type type: string
        @param type: the type of the object (KAF or NAF)
        '''
        if node is None:
            node = ET.Element('statement_source')
            node.set('type', type)
        self.node = node
        self.type = node.get('type', type)
        self.span = None
        span_node = self.node.find('span')
        if span_node is not None:
            from Cspan import Cspan
            self.span = Cspan(span_node, self.type)

    def get_node(self):
        '''
        Returns the node of the element
        @rtype: xml Element
        @return: the node of the element
        '''
        return self.node

    def get_span(self):
        '''
        Returns the span of the statement_source element
        @rtype: L{Cspan}
        @return: span object
        '''
        return self.span

    def set_span(self, my_span):
        '''
        Sets the id of the element
        @type my_span: L{Cspan}
        @param my_span: the span of the statement_source
        '''
        if self.span is not None:
            try:
                self.node.remove(self.span.get_node())
            except ValueError:
                pass
        self.span = my_span
        self.node.append(my_span.get_node())