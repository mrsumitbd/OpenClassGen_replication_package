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
        self.name = iface['name']
        self.contract = contract
        self.functions = []
        
        for func_dict in iface.get('functions', []):
            function_obj = Function(func_dict, self)
            self.functions.append(function_obj)

    def function(self, func_name):
        '''
        Returns the Function instance associated with the given func_name, or raises a
        RpcException if no function matches.
        '''
        for func in self.functions:
            if func.name == func_name:
                return func
        raise RpcException("Function '%s' not found on interface '%s'" % (func_name, self.name))