class FakeLock(object):
    '''
    This is a dummy lock to disable locking of the IB socket connection, which
    is slow and unnecessary. https://github.com/InteractiveBrokers/tws-api/issues/464
    '''

    def acquire(self):
        return True

    def release(self):
        pass