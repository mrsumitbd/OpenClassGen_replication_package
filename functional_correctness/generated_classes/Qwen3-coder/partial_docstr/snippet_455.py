class FieldMetaType(object):
    '''
  Public values for the field data types. Valid types are:

    - ``string``
    - ``datetime``
    - ``int``
    - ``float``
    - ``bool``
    - ``list``
    - ``sdr``
  '''

    STRING = 'string'
    DATETIME = 'datetime'
    INT = 'int'
    FLOAT = 'float'
    BOOL = 'bool'
    LIST = 'list'
    SDR = 'sdr'

    _VALID_TYPES = {STRING, DATETIME, INT, FLOAT, BOOL, LIST, SDR}

    @classmethod
    def isValid(cls, fieldDataType):
        '''Check a candidate value whether it's one of the valid field data types

        :param fieldDataType: (string) candidate field data type
        :returns: True if the candidate value is a legitimate field data type value;
                  False if not
        '''
        return fieldDataType in cls._VALID_TYPES