class MethodLookup:

    def setup_cache(self):
        import random
        random.seed(0)

    def time_lookup_iloc(self, s):
        import random
        from timeit import default_timer as timer
        n = min(1000, len(s))
        positions = random.sample(range(len(s)), n)
        start = timer()
        for pos in positions:
            _ = s.iloc[pos]
        return timer() - start

    def time_lookup_loc(self, s):
        import random
        from timeit import default_timer as timer
        n = min(1000, len(s))
        labels = random.sample(list(s.index), n)
        start = timer()
        for label in labels:
            _ = s.loc[label]
        return timer() - start