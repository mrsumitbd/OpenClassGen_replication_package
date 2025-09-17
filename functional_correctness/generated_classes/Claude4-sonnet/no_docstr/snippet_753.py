class IsInLongSeriesLookUpDominates:
    def setup(self, dtype, MaxNumber, series_type):
        np.random.seed(1234)
        self.N = 10**7
        self.K = 10**6
        
        if series_type == 'object':
            self.series = pd.Series(np.random.choice(['foo', 'bar', 'baz'] * 1000, self.N))
            self.values = ['foo', 'bar']
        elif series_type == 'int64':
            self.series = pd.Series(np.random.randint(0, MaxNumber, self.N))
            self.values = np.random.randint(0, MaxNumber, self.K)
        elif series_type == 'float64':
            self.series = pd.Series(np.random.randn(self.N))
            self.values = np.random.randn(self.K)
        else:
            self.series = pd.Series(np.random.randint(0, MaxNumber, self.N), dtype=dtype)
            self.values = np.random.randint(0, MaxNumber, self.K)

    def time_isin(self, dtypes, MaxNumber, series_type):
        self.series.isin(self.values)