class classproperty(object):
    def __init__(self, getter):
        self.fget = getter

    def __get__(self, instance, owner):
        return self.fget(owner)