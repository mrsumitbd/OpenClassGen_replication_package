class FormatSpecification(object):
    '''The format specification.'''

    def __init__(self, identifier, text_format=False):
        '''Initializes a format specification.

        Args:
          identifier (str): unique name for the format.
          text_format (Optional[bool]): True if the format is a text format,
              False otherwise.
        '''
        if not isinstance(identifier, str):
            raise TypeError("identifier must be a string")
        if not isinstance(text_format, bool):
            raise TypeError("text_format must be a bool")
        self.identifier = identifier
        self._text_format = text_format
        self._signatures = []

    def AddNewSignature(self, pattern, offset=None):
        '''Adds a signature.

        Args:
          pattern (bytes): pattern of the signature.
          offset (int): offset of the signature. None is used to indicate
              the signature has no offset. A positive offset is relative from
              the start of the data a negative offset is relative from the end
              of the data.
        '''
        if not isinstance(pattern, (bytes, bytearray)):
            raise TypeError("pattern must be bytes or bytearray")
        if offset is not None and not isinstance(offset, int):
            raise TypeError("offset must be an int or None")
        # store as bytes
        self._signatures.append((bytes(pattern), offset))

    def IsTextFormat(self):
        '''Determines if the format is a text format.

        Returns:
          bool: True if the format is a text format, False otherwise.
        '''
        return self._text_format