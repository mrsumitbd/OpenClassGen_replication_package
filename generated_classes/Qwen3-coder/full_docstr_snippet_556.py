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
        self.functions = []
        
        # Create Function objects for each function in the interface
        for func_dict in iface.get('functions', []):
            from barrister import Function  # Assuming Function class is in barrister module
            func = Function(func_dict, self)
            self.functions.append(func)

    def function(self, func_name):
        '''
        Returns the Function instance associated with the given func_name, or raises a
        RpcException if no function matches.
        '''
        for func in self.functions:
            if func.func.get('name') == func_name:
                return func
        
        # If we get here, no function was found
        from barrister import RpcException  # Assuming RpcException is in barrister module
        raise RpcException("Function '%s' not found" % func_name)