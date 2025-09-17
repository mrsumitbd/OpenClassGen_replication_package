class Interface(object):
    '''
    Represents a Barrister IDL 'interface' entity.
    '''

    def __init__(self, iface, contract):
        '''
        Creates an Interface. Creates a 'functions' list of Function objects for
        each function defined on the interface.

        :Parameters:
          iface
            Dict representing the interface (from parsed IDL)
          contract
            Contract instance to associate the interface instance with
        '''
        self.iface = iface
        self.contract = contract
        self.name = iface.get('name')
        self.functions = []
        self._func_map = {}
        for f in iface.get('functions', []):
            fn = Function(f, self)
            self.functions.append(fn)
            self._func_map[fn.name] = fn

    def function(self, func_name):
        '''
        Returns the Function instance associated with the given func_name, or raises a
        RpcException if no function matches.
        '''
        if func_name in self._func_map:
            return self._func_map[func_name]
        raise RpcException("Unknown function '%s' in interface '%s'" %
                           (func_name, self.name))