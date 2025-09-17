class ItemGetter(object):
    '''Default `Map` item getter.

    Treats data as a dict and invokes ``data.get`` with ``item.src`` key.
    '''

    def get(self, data, item):
        '''Get corresponding data for an item.

        Subclasses can override this method to implement map access to more complex
        structures than plain dict.

        :param data: source data.
        :param item: item to get.
        '''
        if data is None:
            return None
        try:
            return data.get(item.src)
        except Exception:
            return None

    def to_dict(self, data, multi=False):
        '''Returns map data as a dict.'''
        if multi:
            if data is None:
                return []
            result = []
            for element in data:
                result.append(self.to_dict(element, multi=False))
            return result

        if data is None:
            return {}
        # If it's already a dict or mapping, make a shallow copy
        try:
            return dict(data)
        except Exception:
            return {}