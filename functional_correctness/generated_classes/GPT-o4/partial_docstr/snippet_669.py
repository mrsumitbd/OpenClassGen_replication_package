class FieldMetaSpecial(object):
    '''
  Public values for the "special" field attribute. Valid values are:

    - ``R``: reset
    - ``S``: sequence
    - ``T``: timestamp
    - ``C``: category
    - ``L``: learning
  '''
    R = 'R'
    S = 'S'
    T = 'T'
    C = 'C'
    L = 'L'
    _VALID = {R, S, T, C, L}

    @classmethod
    def isValid(cls, attr):
        '''Check a candidate value whether it's one of the valid attributes

        :param attr: (string) candidate value
        :returns: True if the candidate value is a legitimate "special" field
                  attribute; False if not
        '''
        return isinstance(attr, str) and attr in cls._VALID