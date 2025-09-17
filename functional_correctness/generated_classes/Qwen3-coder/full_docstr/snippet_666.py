class InstanceIterator(object):
    '''
    Iterator for rows in an Instances object.
    '''

    def __init__(self, data):
        '''
        Initializes the iterator.

        :param data: the Instances object to iterate over
        :type data: Instances
        '''
        self._data = data
        self._index = 0

    def __iter__(self):
        '''
        Returns itself.
        '''
        return self

    def next(self):
        '''
        Returns the next row from the Instances object.

        :return: the next Instance object
        :rtype: Instance
        '''
        if self._index >= len(self._data):
            raise StopIteration
        instance = self._data.instance(self._index)
        self._index += 1
        return instance