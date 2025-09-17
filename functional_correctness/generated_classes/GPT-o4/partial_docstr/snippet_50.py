class ColumnDescriptor(object):
    """
    Handles the reading and writing of column values to and from
    a model instance's value manager, as well as creating
    comparator queries.
    """
    def __init__(self, column):
        """
        :param column: columns.Column instance
        """
        self.column = column
        # the name under which this column's value is stored on the instance
        self.name = column.name

    def __get__(self, instance, owner):
        """
        Returns either the column (when accessed on the class) or the
        stored value (when accessed on an instance).
        """
        if instance is None:
            return self.column
        # assume instance._values is a dict-like value manager
        return instance._values.get(self.name, None)

    def __set__(self, instance, value):
        """
        Sets the value on an instance. Raises if attempted on the class.
        """
        if instance is None:
            raise AttributeError(
                "Cannot set column value on the class itself."
            )
        # store the value in the instance's value manager
        instance._values[self.name] = value

    def __delete__(self, instance):
        """
        Sets the column value to None, if the column is nullable.
        """
        if instance is None:
            raise AttributeError(
                "Cannot delete column value on the class itself."
            )
        # check nullable property if present
        nullable = getattr(self.column, 'nullable', True)
        if not nullable:
            raise AttributeError(
                "Column '%s' is not nullable, cannot delete." % self.name
            )
        instance._values[self.name] = None