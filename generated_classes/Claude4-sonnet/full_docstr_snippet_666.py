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
        self.data = data
        self.index = 0

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
        if self.index >= len(self.data):
            raise StopIteration
        instance = self.data[self.index]
        self.index += 1
        return instance