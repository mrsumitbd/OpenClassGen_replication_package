class OneHot(object):
    def __init__(self, n_features, weights=None):
        self.n_features = n_features
        self.weights = weights
        self._output = None
    
    def output(self, dropout_active=False):
        if self._output is None:
            import numpy as np
            self._output = np.eye(self.n_features)
        
        if dropout_active and self.weights is not None:
            return self._output * self.weights
        
        return self._output