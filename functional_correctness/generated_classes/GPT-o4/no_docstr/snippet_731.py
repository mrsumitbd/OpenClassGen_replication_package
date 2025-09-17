class _missing_ctypes(object):

    def cast(self, num, obj):
        raise ImportError("ctypes.cast is not available because the ctypes module could not be imported")

    def c_void_p(self, num):
        raise ImportError("ctypes.c_void_p is not available because the ctypes module could not be imported")