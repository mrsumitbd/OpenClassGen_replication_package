class _Creator:
    '''
    DO NOT REUSE THIS CLASS. Provided for backwards compatibility only!

    A placeholder class that provides a way to set the attribute on the model.
    '''

    def __init__(self, field):
        self.field = field

    def __get__(self, obj, type=None):
        return self

    def __set__(self, obj, value):
        setattr(obj, self.field.name, value)