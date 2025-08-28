class Results:
    '''
    Class to contain model results
    Parameters
    ----------
    model : class instance
        the previously specified model instance
    params : array
        parameter estimates from the fit model
    '''

    def __init__(self, model, params, **kwd):
        self.initialize(model, params, **kwd)

    def initialize(self, model, params, **kwd):
        self.model = model
        self.params = params
        for key, value in kwd.items():
            setattr(self, key, value)