class _BaseDevice(object):
    '''Parent class for the dynamic Device class.

    The Device class being made of whatever fields the Spark Cloud API gives us,
    it has to be contructed on the fly once we know those fields.

    The generated Device class is subclassing this _BaseDevice as well as a
    nametuple.

    The namedtuple host all static fields while _BaseDevice host methods
    extending how a Device object should behave.
    '''

    @staticmethod
    def make_device_class(spark_cloud, entries, timeout=30):
        '''Returns a dynamic Device class based on what a GET device list from
        the Spark Cloud returns.

        spark_cloud parameter should be the caller instance of SparkCloud.
        entries parameter should be the list of fields the Spark Cloud API is
        returning.
        '''
        # create a namedtuple with the given entries
        BaseTuple = namedtuple('Device', entries)
        # build a new class that inherits from both BaseTuple and _BaseDevice
        attrs = {
            '_spark': spark_cloud,
            '_timeout': timeout,
        }
        return type('Device', (BaseTuple, _BaseDevice), attrs)

    def __getattr__(self, name):
        '''Returns virtual attributes corresponding to function or variable
        names.
        '''
        # dynamic function call
        funcs = getattr(self, 'functions', [])
        if name in funcs:
            def fcall(*args):
                return self._spark.call_function(self.id, name, args, self._timeout)
            return fcall

        # dynamic variable lookup
        vars_ = getattr(self, 'variables', [])
        if name in vars_:
            return self._spark.get_variable(self.id, name)

        raise AttributeError(f"{type(self).__name__!r} object has no attribute {name!r}")