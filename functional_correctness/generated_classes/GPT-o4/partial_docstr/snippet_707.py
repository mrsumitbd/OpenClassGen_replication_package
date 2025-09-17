class BaseDirective(object):
    '''
    Every Directive has to provide the following Attributes/Methods:

    * ``name`` (like ``.set``)
    * ``get_words(line)``: return the data to store
    * ``get_word_count(line)``: return the number of words to store
    * ``isstatic()`` returns True, if the reference should be static
    '''

    def __init__(self, name):
        self.name = name

    def get_words(self, line):
        raise NotImplementedError("Subclasses must implement get_words()")

    def get_word_count(self, line):
        raise NotImplementedError("Subclasses must implement get_word_count()")

    def isstatic(self):
        raise NotImplementedError("Subclasses must implement isstatic()")