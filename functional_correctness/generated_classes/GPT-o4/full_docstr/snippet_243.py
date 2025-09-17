class TimeFormat:
    '''
    Time-based benchmarks for format operations
    These are emphasized because they will have the greatest impact on end users
    '''

    def setup(self):
        '''
            General setup functions
        '''
        class Counter:
            def __init__(self, total):
                self.count = 0
                self.total = total
            def format(self):
                return "[{count:>7}/{total}]".format(count=self.count, total=self.total)
        self.Counter = Counter
        self.total = 1000
        self.bar = Counter(self.total)
        self.counter = Counter(self.total)

    def time_format_bar(self):
        '''
            Time Counter.format() for progress bar
            Count does not exceed total
        '''
        for i in range(self.total):
            self.bar.count = i
            self.bar.format()

    def time_format_counter(self):
        '''
            Time Counter.format() for counter
            Count exceeds total
        '''
        for i in range(self.total):
            self.counter.count = self.total + i
            self.counter.format()

    def time_format_status_bar(self):
        '''
            Time Counter.format() for status bar
            Uses dynamic variable
        '''
        for i in range(self.total):
            width = (i % 10) + 1
            "[{count:>{w}}/{total}]".format(count=i, w=width, total=self.total)