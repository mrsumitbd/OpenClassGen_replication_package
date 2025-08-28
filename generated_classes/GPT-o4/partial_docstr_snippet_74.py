class Term:
    '''
    Base class for the terms of a TDL conjunction.

    All terms are defined to handle the binary '&' operator, which
    puts both into a Conjunction:

    >>> TypeIdentifier('a') & TypeIdentifier('b')
    <Conjunction object at 140008950372168>

    Args:
        docstring (str): documentation string

    Attributes:
        docstring (str): documentation string
    '''

    def __init__(self, docstring=None):
        self.docstring = docstring

    def __repr__(self):
        cls = self.__class__.__name__
        if self.docstring is None:
            return f"{cls}()"
        return f"{cls}({self.docstring!r})"

    def __and__(self, other):
        from itertools import chain
        from types import SimpleNamespace

        # Lazy import to avoid circularity if Conjunction is in another module
        try:
            Conjunction = globals()['Conjunction']
        except KeyError:
            raise NameError("Conjunction class is not defined")

        # Flatten if chaining multiple &
        if isinstance(self, Conjunction) and isinstance(other, Conjunction):
            terms = list(chain(self.terms, other.terms))
        elif isinstance(self, Conjunction):
            terms = list(self.terms) + [other]
        elif isinstance(other, Conjunction):
            terms = [self] + list(other.terms)
        else:
            terms = [self, other]

        return Conjunction(terms)