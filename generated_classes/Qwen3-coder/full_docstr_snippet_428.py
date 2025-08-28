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
        return data.get(item.src)

    def to_dict(self, data, multi=False):
        '''Returns map data as a dict.'''
        if multi:
            return {key: values for key, values in data.items()}
        else:
            return {key: value for key, value in data.items()}