class HTMLLxmlMixin(object):

    def find_element_by_xpath(self, xpath):
        '''
        Finds an element by xpath.

        :param xpath: The xpath locator of the element to find.
        :return: ElemLxml

        See lxml xpath expressions `here <http://lxml.de/xpathxslt.html#xpath>`_
        '''
        elements = self.xpath(xpath)
        if elements:
            return elements[0]
        return None

    def find_elements_by_xpath(self, xpath):
        '''
        Finds multiple elements by xpath.

        :param xpath: The xpath locator of the elements to be found.
        :return: list of ElemLxml

        See lxml xpath expressions `here <http://lxml.de/xpathxslt.html#xpath>`_
        '''
        return self.xpath(xpath)