class JavaArrayIterator(object):
    '''
    Iterator for elements in a Java array.
    '''

    def __init__(self, data):
        '''
        :param data: the Java array to iterate over
        :type data: JavaArray
        '''
        self.data = data
        self.index = 0
        self.length = data.length if hasattr(data, 'length') else len(data)

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
        if self.index >= self.length:
            raise StopIteration
        
        try:
            element = self.data[self.index]
        except (IndexError, AttributeError):
            raise StopIteration
            
        self.index += 1
        return element