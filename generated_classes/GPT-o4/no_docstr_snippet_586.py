class get_all_functions_args(object):
    """
    Attributes:
     - (none)
    """

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()
        self.validate()

    def write(self, oprot):
        self.validate()
        oprot.writeStructBegin('get_all_functions_args')
        # no fields
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        # no required fields to check
        return

    def __repr__(self):
        return 'get_all_functions_args()'

    def __eq__(self, other):
        return isinstance(other, get_all_functions_args)

    def __ne__(self, other):
        return not self.__eq__(other)