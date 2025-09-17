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
        self._id = None

    def get_id(self):
        '''
        Getter for 'id' field.
        :return: value of 'id' field.
        '''
        return self._id

    def set_id(self, value):
        '''
        Setter for 'id' field.
        :param value: a new value of 'id' field. Must be either None (ID is optional according to BPMN 2.0 XML Schema)
                      or String type.
        '''
        if value is not None and not isinstance(value, str):
            raise TypeError("id must be a string or None")
        self._id = value

    id = property(get_id, set_id)