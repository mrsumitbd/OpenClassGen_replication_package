class OneHot(object):
    def __init__(self, n_features, weights=None):
        self.n_features = n_features
        if weights is None:
            self.keep_probs = np.ones(self.n_features, dtype=float)
        else:
            w = np.array(weights, dtype=float)
            if w.ndim == 0:
                w = np.full(self.n_features, w, dtype=float)
            if w.shape != (self.n_features,):
                raise ValueError("weights must be a scalar or array of length n_features")
            self.keep_probs = w

    def output(self, dropout_active=False):
        if dropout_active:
            mask = np.random.binomial(1, self.keep_probs)
            # Inverted dropout scaling
            mask = mask / self.keep_probs
        else:
            mask = np.ones(self.n_features, dtype=float)
        return np.diag(mask)