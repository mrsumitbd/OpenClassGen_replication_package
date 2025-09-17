class ZOSPropMapper(object):
    '''Descriptor for mapping ZOS object properties to corresponding wrapper classes
    '''

    def __init__(self, zos_interface_attr, property_name, setter=False, cast_to=None):
        '''
        @param zos_interface_attr : attribute used to dispatch method/property calls to 
        the zos_object (it hold the zos_object)
        @param propname : string, like 'SystemName' for IOpticalSystem
        @param setter : if False, a read-only data descriptor is created
        @param cast_to : Name of class (generally the base class) whose property to call
        '''
        self.zos_interface_attr = zos_interface_attr
        self.property_name = property_name
        self.setter = setter
        self.cast_to = cast_to

    def __get__(self, obj, objtype):
        if obj is None:
            return self
        zos_interface = getattr(obj, self.zos_interface_attr)
        if self.cast_to:
            zos_interface = getattr(zos_interface, self.cast_to)
        return getattr(zos_interface, self.property_name)

    def __set__(self, obj, value):
        if not self.setter:
            raise AttributeError("can't set attribute")
        zos_interface = getattr(obj, self.zos_interface_attr)
        if self.cast_to:
            zos_interface = getattr(zos_interface, self.cast_to)
        setattr(zos_interface, self.property_name, value)