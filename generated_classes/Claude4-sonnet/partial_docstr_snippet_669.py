class FieldMetaSpecial(object):
    '''
  Public values for the "special" field attribute. Valid values are:

    - ``R``: reset
    - ``S``: sequence
    - ``T``: timestamp
    - ``C``: category
    - ``L``: learning
  '''

    @classmethod
    def isValid(cls, attr):
        '''Check a candidate value whether it's one of the valid attributes

        :param attr: (string) candidate value
        :returns: True if the candidate value is a legitimate "special" field
                  attribute; False if not
        '''
        valid_attrs = {'R', 'S', 'T', 'C', 'L'}
        return attr in valid_attrs