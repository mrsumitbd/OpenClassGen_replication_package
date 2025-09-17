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
        if self.index >= len(self.data):
            raise StopIteration
        
        element = self.data[self.index]
        self.index += 1
        return element