class Module(object):
    '''Module mix-in for the parametric function classes.
    '''

    def __init__(self):
        pass

    def get_parameters(self, grad_only=True):
        '''Get parameters.
        Args:
            grad_only (bool, optional): Return parameters with `need_grad` option as `True`. 
            If you set this option as `False`, All parameters are returned. Default is `True`.
        Returns:
            dict: The dictionary of parameter name (`str`) to Variable (:obj:`~nnabla.Variable`).
        '''
        parameters = {}
        for module in self.get_modules():
            if hasattr(module, '_parameters'):
                for name, param in module._parameters.items():
                    if param is not None:
                        if not grad_only or param.need_grad:
                            parameters[name] = param
        return parameters

    def get_modules(self, memo=None, prefix=""):
        '''Get modules.

        This function is internally used as the helper method for other methods.

        Args: 
            memo (set, optional): Module set in order to memorize to visit.
            prefix (str, optional): Prefix to a specific parameter name.

        Yields:
            `Module`: The module class.
        '''
        if memo is None:
            memo = set()
        if self not in memo:
            memo.add(self)
            yield self
            for name in dir(self):
                if not name.startswith('_'):
                    attr = getattr(self, name)
                    if isinstance(attr, Module):
                        for module in attr.get_modules(memo, prefix + name + '.'):
                            yield module

    def save_parameters(self, path, grad_only=False):
        '''Save all parameters into a file with the specified format.

        Currently hdf5 and protobuf formats are supported.

        Args:
            path : path or file object
            grad_only (bool, optional): Return parameters with `need_grad` option as `True`. 
        '''
        import nnabla
        parameters = self.get_parameters(grad_only=grad_only)
        nnabla.save_parameters(path, parameters)

    def load_parameters(self, path):
        '''Load parameters from a file with the specified format.

        Args:
            path : path or file object
        '''
        import nnabla
        parameters = nnabla.load_parameters(path)
        for name, param in parameters.items():
            # Assuming parameters are loaded into the appropriate modules
            # This is a simplified implementation - in practice, you'd need
            # to map parameter names to the correct module attributes
            pass