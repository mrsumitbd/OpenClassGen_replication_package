class ItemGetter(object):
    '''Default `Map` item getter.

    Treats data as a dict and invokes ``data.get`` with ``item.src`` key.
    '''

    def get(self, data, item):
        '''Get corresponding data for an item.

        Subsclasses can override this method to implement map access to more complex
        structures then plain dict.

        :param data: source data.
        :param item: item to get.
        '''
        if hasattr(data, 'get'):
            return data.get(item.src)
        else:
            return getattr(data, item.src, None)

    def to_dict(self, data, multi=False):
        '''Returns map data as a dict.'''
        if hasattr(data, 'to_dict'):
            return data.to_dict(multi=multi)
        elif isinstance(data, dict):
            return data
        else:
            return dict(data) if data else {}