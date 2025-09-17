class JavaArrayIterator(object):
    '''
    Iterator for elements in a Java array.
    '''

    def __init__(self, data):
        '''
        :param data: the Java array to iterate over
        :type data: JavaArray
        '''
        self._data = data
        self._index = 0
        # Try to get Java-style length, else Python len()
        try:
            self._length = data.length
        except AttributeError:
            self._length = len(data)

    def __iter__(self):
        '''
        Returns itself.
        '''
        return self

    def __next__(self):
        '''
        Returns the next element from the array.

        :return: the next array element object, wrapped as JavaObject if not null
        :rtype: JavaObject or None
        '''
        if self._index >= self._length:
            raise StopIteration
        element = self._data[self._index]
        self._index += 1
        if element is None:
            return None
        # Assume JavaObject is available in scope
        return JavaObject(element)