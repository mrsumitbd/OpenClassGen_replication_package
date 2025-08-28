class TimeFormat:
    '''
    Time-based benchmarks for format operations
    These are emphasized because they will have the greatest impact on end users
    '''

    def setup(self):
        '''
        General setup functions
        '''
        self.counter_bar = tqdm(total=1000, desc="Progress", leave=False)
        self.counter_bar.n = 500
        
        self.counter_exceed = tqdm(total=100, desc="Counter", leave=False)
        self.counter_exceed.n = 150
        
        self.status_bar = tqdm(total=None, desc="Status", leave=False)
        self.status_bar.n = 42
        self.dynamic_var = "Processing files"

    def time_format_bar(self):
        '''
        Time Counter.format() for progress bar
        Count does not exceed total
        '''
        return self.counter_bar.format_meter(
            n=self.counter_bar.n,
            total=self.counter_bar.total,
            elapsed=time.time() - self.counter_bar.start_t if hasattr(self.counter_bar, 'start_t') else 10.5,
            ncols=80,
            prefix=self.counter_bar.desc
        )

    def time_format_counter(self):
        '''
        Time Counter.format() for counter
        Count exceeds total
        '''
        return self.counter_exceed.format_meter(
            n=self.counter_exceed.n,
            total=self.counter_exceed.total,
            elapsed=time.time() - self.counter_exceed.start_t if hasattr(self.counter_exceed, 'start_t') else 15.2,
            ncols=80,
            prefix=self.counter_exceed.desc
        )

    def time_format_status_bar(self):
        '''
        Time Counter.format() for status bar
        Uses dynamic variable
        '''
        return self.status_bar.format_meter(
            n=self.status_bar.n,
            total=self.status_bar.total,
            elapsed=time.time() - self.status_bar.start_t if hasattr(self.status_bar, 'start_t') else 8.7,
            ncols=80,
            prefix=f"{self.status_bar.desc}: {self.dynamic_var}"
        )