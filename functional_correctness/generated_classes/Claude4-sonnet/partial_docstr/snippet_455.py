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

    string = "string"
    datetime = "datetime"
    integer = "int"
    float = "float"
    boolean = "bool"
    list = "list"
    sdr = "sdr"

    @classmethod
    def isValid(cls, fieldDataType):
        '''Check a candidate value whether it's one of the valid field data types

        :param fieldDataType: (string) candidate field data type
        :returns: True if the candidate value is a legitimate field data type value;
                  False if not
        '''
        valid_types = {"string", "datetime", "int", "float", "bool", "list", "sdr"}
        return fieldDataType in valid_types