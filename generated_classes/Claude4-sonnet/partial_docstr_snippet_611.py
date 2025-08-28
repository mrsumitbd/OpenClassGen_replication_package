class _Clock(object):
    '''A clock to determine the current time, in seconds.'''

    def now(self):
        '''Returns the number of seconds since epoch.'''
        return time.time()

    def sleep(self, seconds):
        '''Sleeps for the desired number of seconds.'''
        time.sleep(seconds)