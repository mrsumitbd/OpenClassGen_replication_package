class BaseElement(object):
    '''
    Class used for representing tBaseElement of BPMN 2.0 graph.
    Fields:
    - id: an ID of element. Must be either None (ID is optional according to BPMN 2.0 XML Schema) or String.
    '''

    def __init__(self):
        '''
        Default constructor, initializes object fields with new instances.
        '''
        self.id = None

    def get_id(self):
        '''
        Getter for 'id' field.
        :return: value of 'id' field.
        '''
        return self.id

    def set_id(self, value):
        '''
        Setter for 'id' field.
        :param value - a new value of 'id' field. Must be either None (ID is optional according to BPMN 2.0 XML Schema)
        or String type.
        '''
        self.id = value