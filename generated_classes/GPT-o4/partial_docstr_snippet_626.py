class ZOSPropMapper(object):
    '''Descriptor for mapping ZOS object properties to corresponding wrapper classes
    '''

    def __init__(self, zos_interface_attr, property_name, setter=False, cast_to=None):
        self.zos_interface_attr = zos_interface_attr
        self.property_name = property_name
        self.setter = setter
        self.cast_to = cast_to

    def __get__(self, obj, objtype):
        if obj is None:
            return self
        iface = getattr(obj, self.cast_to) if self.cast_to else getattr(obj, self.zos_interface_attr)
        return getattr(iface, self.property_name)

    def __set__(self, obj, value):
        if not self.setter:
            raise AttributeError("can't set attribute")
        iface = getattr(obj, self.cast_to) if self.cast_to else getattr(obj, self.zos_interface_attr)
        setattr(iface, self.property_name, value)