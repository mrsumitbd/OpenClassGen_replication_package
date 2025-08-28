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
        DeviceTuple = namedtuple('DeviceTuple', entries)
        
        class Device(_BaseDevice, DeviceTuple):
            def __new__(cls, *args, **kwargs):
                return DeviceTuple.__new__(cls, *args, **kwargs)
            
            def __init__(self, *args, **kwargs):
                self._spark_cloud = spark_cloud
                self._timeout = timeout
        
        return Device

    def __getattr__(self, name):
        '''Returns virtual attributes corresponding to function or variable
        names.
        '''
        if hasattr(self, 'functions') and name in self.functions:
            def fcall(*args):
                return self._spark_cloud.call_function(self.id, name, *args, timeout=self._timeout)
            return fcall
        elif hasattr(self, 'variables') and name in self.variables:
            return self._spark_cloud.get_variable(self.id, name, timeout=self._timeout)
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")