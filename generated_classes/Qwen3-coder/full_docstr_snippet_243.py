class TimeFormat:
    '''
    Time-based benchmarks for format operations
    These are emphasized because they will have the greatest impact on end users
    '''

    def setup(self):
        '''
        General setup functions
        '''
        from collections import Counter
        self.counter = Counter()
        self.counter.count = 50
        self.counter.total = 100
        
        # For counter test where count exceeds total
        self.overflow_counter = Counter()
        self.overflow_counter.count = 150
        self.overflow_counter.total = 100
        
        # For status bar with dynamic variable
        self.status_counter = Counter()
        self.status_counter.count = 75
        self.status_counter.total = 100
        self.status_counter.desc = "Processing"

    def time_format_bar(self):
        '''
        Time Counter.format() for progress bar
        Count does not exceed total
        '''
        self.counter.format()

    def time_format_counter(self):
        '''
        Time Counter.format() for counter
        Count exceeds total
        '''
        self.overflow_counter.format()

    def time_format_status_bar(self):
        '''
        Time Counter.format() for status bar
        Uses dynamic variable
        '''
        self.status_counter.format()