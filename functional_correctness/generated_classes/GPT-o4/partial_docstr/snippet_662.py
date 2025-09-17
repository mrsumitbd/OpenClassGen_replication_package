class Module(object):
    '''Module mix-in for the parametric function classes.
    '''

    def __init__(self):
        super(Module, self).__init__()

    def get_parameters(self, grad_only=True):
        params = {}
        for prefix, module in self.get_modules(prefix=""):
            for name, val in module.__dict__.items():
                if isinstance(val, nn.Variable):
                    if not grad_only or val.need_grad:
                        params[prefix + name] = val
        return params

    def get_modules(self, memo=None, prefix=""):
        if memo is None:
            memo = set()
        if self in memo:
            return
        memo.add(self)
        yield prefix, self
        for name, val in self.__dict__.items():
            if isinstance(val, Module):
                sub_prefix = prefix + name + "."
                for item in val.get_modules(memo, sub_prefix):
                    yield item

    def save_parameters(self, path, grad_only=False):
        params = self.get_parameters(grad_only)
        save_parameters(params, path)

    def load_parameters(self, path):
        params = self.get_parameters(grad_only=False)
        nnabla_load_parameters(path, params)