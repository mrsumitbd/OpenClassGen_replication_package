class get_all_functions_args(object):

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == 0:
                break
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        oprot.writeStructBegin('get_all_functions_args')
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        return '<get_all_functions_args>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return True

    def __ne__(self, other):
        return not (self == other)