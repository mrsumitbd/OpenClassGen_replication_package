class ARIMA(object):
    '''A Wrapper for the statsmodels.tsa.arima_model.ARIMA class.'''

    def __init__(self, p, d, q, steps):
        '''Initialize the ARIMA object.

        Args:
            p (int):
                Integer denoting the order of the autoregressive model.
            d (int):
                Integer denoting the degree of differencing.
            q (int):
                Integer denoting the order of the moving-average model.
            steps (int):
                Integer denoting the number of time steps to predict ahead.
        '''
        self.p = p
        self.d = d
        self.q = q
        self.steps = steps

    def predict(self, X):
        '''Predict values using the initialized object.

        Args:
            X (ndarray):
                N-dimensional array containing the input sequences for the model.

        Returns:
            ndarray:
                N-dimensional array containing the predictions for each input sequence.
        '''
        if X.ndim == 1:
            X = X.reshape(1, -1)
        
        predictions = []
        
        for sequence in X:
            model = StatsARIMA(sequence, order=(self.p, self.d, self.q))
            fitted_model = model.fit()
            forecast = fitted_model.forecast(steps=self.steps)
            predictions.append(forecast)
        
        return np.array(predictions)