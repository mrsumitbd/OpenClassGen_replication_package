class AttrList:
    """
    A filtered attribute list.
    Items are included during iteration if they are in either the (xs) or
    (xml) namespaces.
    @ivar raw: The raw attribute list.
    @type raw: list
    """

    # XML and XML-Schema-instance namespace URIs
    XS_NS = "http://www.w3.org/2001/XMLSchema-instance"
    XML_NS = "http://www.w3.org/XML/1998/namespace"

    def __init__(self, attributes):
        """
        @param attributes: A list of attributes
        @type attributes: list
        """
        self.raw = list(attributes)

    def real(self):
        """
        Get list of real attributes which exclude xs and xml attributes.
        @return: A list of real attributes.
        @rtype: generator
        """
        return (attr for attr in self.raw if not self.skip(attr))

    def rlen(self):
        """
        Get the number of real attributes which exclude xs and xml attributes.
        @return: A count of real attributes.
        @rtype: int
        """
        return sum(1 for _ in self.real())

    def lang(self):
        """
        Get list of filtered attributes which exclude xs.
        @return: A list of filtered attributes.
        @rtype: generator
        """
        return (
            attr
            for attr in self.raw
            if getattr(attr, "namespace", None) != self.XS_NS
        )

    def skip(self, attr):
        """
        Get whether to skip (filter-out) the specified attribute.
        @param attr: An attribute.
        @type attr: Attribute
        @return: True if should be skipped.
        @rtype: bool
        """
        ns = getattr(attr, "namespace", None)
        return ns == self.XS_NS or ns == self.XML_NS