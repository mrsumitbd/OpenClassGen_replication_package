class Module(object):
    '''Module mix-in for the parametric function classes.
    '''

    def __init__(self):
        self._modules = OrderedDict()
        self._parameters = OrderedDict()

    def get_parameters(self, grad_only=True):
        '''Get parameters.
        Args:
            grad_only (bool, optional): Return parameters with `need_grad` option as `True`. 
            If you set this option as `False`, All parameters are returned. Default is `True`.
        Returns:
            dict: The dictionary of parameter name (`str`) to Variable (:obj:`~nnabla.Variable`).
        '''
        params = OrderedDict()
        for name, module in self.get_modules():
            for param_name, param in module._parameters.items():
                if param is not None:
                    if not grad_only or (hasattr(param, 'need_grad') and param.need_grad):
                        full_name = name + '.' + param_name if name else param_name
                        params[full_name] = param
        return params

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
            yield prefix, self
            
            for name, module in self._modules.items():
                if module is None:
                    continue
                submodule_prefix = prefix + ('.' if prefix else '') + name
                for m in module.get_modules(memo, submodule_prefix):
                    yield m

    def save_parameters(self, path, grad_only=False):
        '''Save all parameters into a file with the specified format.

        Currently hdf5 and protobuf formats are supported.

        Args:
            path : path or file object
            grad_only (bool, optional): Return parameters with `need_grad` option as `True`. 
        '''
        params = self.get_parameters(grad_only=grad_only)
        
        if isinstance(path, str):
            if path.endswith('.h5') or path.endswith('.hdf5'):
                with h5py.File(path, 'w') as f:
                    for name, param in params.items():
                        f.create_dataset(name, data=param.d if hasattr(param, 'd') else param)
            else:
                with open(path, 'wb') as f:
                    param_dict = {name: param.d if hasattr(param, 'd') else param for name, param in params.items()}
                    pickle.dump(param_dict, f)
        else:
            param_dict = {name: param.d if hasattr(param, 'd') else param for name, param in params.items()}
            pickle.dump(param_dict, path)

    def load_parameters(self, path):
        '''Load parameters from a file with the specified format.

        Args:
            path : path or file object
        '''
        current_params = self.get_parameters(grad_only=False)
        
        if isinstance(path, str):
            if path.endswith('.h5') or path.endswith('.hdf5'):
                with h5py.File(path, 'r') as f:
                    for name in f.keys():
                        if name in current_params:
                            if hasattr(current_params[name], 'd'):
                                current_params[name].d[...] = f[name][...]
                            else:
                                current_params[name] = f[name][...]
            else:
                with open(path, 'rb') as f:
                    loaded_params = pickle.load(f)
                    for name, value in loaded_params.items():
                        if name in current_params:
                            if hasattr(current_params[name], 'd'):
                                current_params[name].d[...] = value
                            else:
                                current_params[name] = value
        else:
            loaded_params = pickle.load(path)
            for name, value in loaded_params.items():
                if name in current_params:
                    if hasattr(current_params[name], 'd'):
                        current_params[name].d[...] = value
                    else:
                        current_params[name] = value