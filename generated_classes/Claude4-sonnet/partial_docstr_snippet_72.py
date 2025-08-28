class FakeLock(object):
    '''
    This is a dummy lock to disable locking of the IB socket connection, which
    is slow and unnecessary. https://github.com/InteractiveBrokers/tws-api/issues/464
    '''

    def acquire(self):
        pass

    def release(self):
        pass

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
        return False