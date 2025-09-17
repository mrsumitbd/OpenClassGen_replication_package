class ColumnDescriptor(object):
    """
    Handles the reading and writing of column values to and from
    a model instance's value manager, as well as creating
    comparator queries
    """
    def __init__(self, column):
        """
        :param column:
        :type column: columns.Column
        """
        self.column = column
        self.name = column.name

    def __get__(self, instance, owner):
        """
        Returns either the value or column, depending
        on if an instance is provided or not

        :param instance: the model instance
        :type instance: Model
        """
        if instance is None:
            return self.column
        values = getattr(instance, '_values', None)
        if values is None:
            raise AttributeError("Instance has no value manager")
        return values.get(self.name, self.column.default)

    def __set__(self, instance, value):
        """
        Sets the value on an instance, raises an exception with classes
        TODO: use None instance to create update statements
        """
        if instance is None:
            raise AttributeError("Cannot set value on class")
        if getattr(self.column, 'read_only', False) and self.name in getattr(instance, '_values', {}):
            raise AttributeError("Column '%s' is read-only" % self.name)
        if not hasattr(instance, '_values'):
            setattr(instance, '_values', {})
        instance._values[self.name] = value

    def __delete__(self, instance):
        """
        Sets the column value to None, if possible
        """
        if instance is None:
            raise AttributeError("Cannot delete column on class")
        if getattr(self.column, 'read_only', False):
            raise AttributeError("Column '%s' is read-only" % self.name)
        if not getattr(self.column, 'nullable', True):
            raise AttributeError("Column '%s' is not nullable" % self.name)
        if not hasattr(instance, '_values'):
            setattr(instance, '_values', {})
        instance._values[self.name] = None