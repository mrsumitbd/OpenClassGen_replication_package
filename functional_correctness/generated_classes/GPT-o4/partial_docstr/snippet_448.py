class HTMLLxmlMixin(object):

    def _get_lxml_tree(self):
        return html.fromstring(self.html)

    def find_element_by_xpath(self, xpath):
        elems = self._get_lxml_tree().xpath(xpath)
        if not elems:
            return None
        return ElemLxml(elems[0])

    def find_elements_by_xpath(self, xpath):
        return [ElemLxml(el) for el in self._get_lxml_tree().xpath(xpath)]