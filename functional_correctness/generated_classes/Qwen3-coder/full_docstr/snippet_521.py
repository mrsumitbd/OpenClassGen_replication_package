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
            self.node = etree.Element('statement_target')
        else:
            self.node = node

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
        span_node = self.node.find('span')
        if span_node is not None:
            from span import Cspan
            return Cspan(span_node)
        return None

    def set_span(self, my_span):
        '''
        Sets the id of the element
        @type my_span: L{Cspan}
        @param my_span: the span of the statement_target
        '''
        from span import Cspan
        # Remove existing span if any
        existing_span = self.node.find('span')
        if existing_span is not None:
            self.node.remove(existing_span)
        
        # Add the new span
        self.node.append(my_span.get_node())