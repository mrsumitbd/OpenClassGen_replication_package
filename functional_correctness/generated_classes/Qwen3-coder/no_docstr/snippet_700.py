class MethodLookup:
    def setup_cache(self):
        self.s = pd.Series(np.random.randn(1000000))
        self.s.index = pd.date_range('2000-01-01', periods=len(self.s), freq='D')
        self.lookup_index = len(self.s) // 2
        self.lookup_label = self.s.index[len(self.s) // 2]

    def time_lookup_iloc(self, s):
        _ = s.iloc[self.lookup_index]

    def time_lookup_loc(self, s):
        _ = s.loc[self.lookup_label]