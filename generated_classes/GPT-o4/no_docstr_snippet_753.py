class IsInLongSeriesLookUpDominates:

    def setup(self, dtype, MaxNumber, series_type):
        # create base data array
        data = np.arange(MaxNumber, dtype=dtype)
        # build the series or list
        if series_type == 'pandas':
            self.series = pd.Series(data)
        else:
            self.series = data.tolist()
        # build lookup values (a subset of the data)
        rng = np.random.RandomState(0)
        cnt = max(1, MaxNumber // 10)
        self.values = rng.choice(data, size=cnt, replace=False)

    def time_isin(self, dtype, MaxNumber, series_type):
        if series_type == 'pandas':
            return self.series.isin(self.values)
        else:
            lookup = set(self.values)
            return [x in lookup for x in self.series]