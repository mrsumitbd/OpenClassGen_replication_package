class FormatSpecification(object):
    '''The format specification.'''

    def __init__(self, identifier, text_format=False):
        '''Initializes a format specification.

        Args:
          identifier (str): unique name for the format.
          text_format (Optional[bool]): True if the format is a text format,
              False otherwise.
        '''
        self.identifier = identifier
        self.text_format = text_format
        self.signatures = []

    def AddNewSignature(self, pattern, offset=None):
        '''Adds a signature.

        Args:
          pattern (bytes): pattern of the signature.
          offset (int): offset of the signature. None is used to indicate
              the signature has no offset. A positive offset is relative from
              the start of the data a negative offset is relative from the end
              of the data.
        '''
        self.signatures.append((pattern, offset))

    def IsTextFormat(self):
        '''Determines if the format is a text format.

        Returns:
          bool: True if the format is a text format, False otherwise.
        '''
        return self.text_format