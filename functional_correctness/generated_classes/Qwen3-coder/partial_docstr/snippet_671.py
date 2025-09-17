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
        from collections import namedtuple
        
        # Create a namedtuple class with the given entries
        DeviceTuple = namedtuple('DeviceTuple', entries)
        
        # Create a dynamic class that inherits from both _BaseDevice and the namedtuple
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
        def fcall(*args):
            # Call the function on the spark cloud with this device's id
            return self._spark_cloud.call_function(self.id, name, args, timeout=self._timeout)
        
        return fcall