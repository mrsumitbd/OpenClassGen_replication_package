class IsInLongSeriesLookUpDominates:
    def setup(self, dtype, MaxNumber, series_type):
        import pandas as pd
        import numpy as np
        
        # Create series based on series_type
        if series_type == 'sorted':
            self.series = pd.Series(np.arange(MaxNumber, dtype=dtype))
        elif series_type == 'reverse_sorted':
            self.series = pd.Series(np.arange(MaxNumber, 0, -1, dtype=dtype))
        else:  # random
            np.random.seed(42)
            self.series = pd.Series(np.random.choice(MaxNumber, size=MaxNumber, replace=False).astype(dtype))
        
        # Create lookup values (small subset for lookup)
        np.random.seed(24)
        self.lookup_values = np.random.choice(self.series.values, size=1000, replace=False)

    def time_isin(self, dtypes, MaxNumber, series_type):
        self.series.isin(self.lookup_values)