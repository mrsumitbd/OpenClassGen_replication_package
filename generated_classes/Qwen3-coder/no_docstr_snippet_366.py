class OneHot(object):
    def __init__(self, n_features, weights=None):
        self.n_features = n_features
        if weights is None:
            self.weights = np.ones(n_features)
        else:
            self.weights = np.array(weights)
            if len(self.weights) != n_features:
                raise ValueError("Length of weights must match n_features")
    
    def output(self, dropout_active=False):
        if dropout_active:
            # Apply dropout by setting some weights to zero
            dropout_mask = np.random.binomial(1, 0.5, self.n_features)
            return self.weights * dropout_mask
        else:
            return self.weights.copy()