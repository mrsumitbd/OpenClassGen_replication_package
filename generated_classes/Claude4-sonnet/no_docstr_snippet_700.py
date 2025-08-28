class MethodLookup:
    def __init__(self):
        self.df = None
        self.series = None

    def setup_cache(self):
        import pandas as pd
        import numpy as np
        
        n = 10000
        self.df = pd.DataFrame({
            'A': np.random.randn(n),
            'B': np.random.randn(n),
            'C': np.random.randn(n)
        })
        self.series = pd.Series(np.random.randn(n))

    def time_lookup_iloc(self, s):
        for i in range(100):
            _ = self.series.iloc[i]

    def time_lookup_loc(self, s):
        for i in range(100):
            _ = self.series.loc[i]