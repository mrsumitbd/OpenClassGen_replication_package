class ColumnDescriptor(object):
    '''
    Handles the reading and writing of column values to and from
    a model instance's value manager, as well as creating
    comparator queries
    '''

    def __init__(self, column):
        '''
        :param column:
        :type column: columns.Column
        :return:
        '''
        self.column = column

    def __get__(self, instance, owner):
        '''
        Returns either the value or column, depending
        on if an instance is provided or not

        :param instance: the model instance
        :type instance: Model
        '''
        if instance is None:
            return self.column
        return instance._values.get(self.column.column_name)

    def __set__(self, instance, value):
        '''
        Sets the value on an instance, raises an exception with classes
        TODO: use None instance to create update statements
        '''
        if instance is None:
            raise AttributeError("Cannot set attribute on class")
        instance._values[self.column.column_name] = value

    def __delete__(self, instance):
        '''
        Sets the column value to None, if possible
        '''
        if instance is None:
            raise AttributeError("Cannot delete attribute on class")
        instance._values[self.column.column_name] = None