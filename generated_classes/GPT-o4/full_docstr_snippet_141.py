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
        arr = np.atleast_2d(X)
        results = []
        for series in arr:
            model = _ARIMA(series, order=(self.p, self.d, self.q))
            fitted = model.fit(disp=0)
            forecast = fitted.forecast(steps=self.steps)[0]
            results.append(forecast)
        return np.array(results)