class _BundleActivator(object):
    '''
    Bundle activator: registers a dummy probe service
    '''

    def __init__(self):
        '''
        Sets up members
        '''
        self._registration = None

    def start(self, context):
        '''
        Bundle started
        '''
        # Register a dummy probe service
        class DummyProbeService(object):
            def probe(self):
                return "dummy"
        
        service = DummyProbeService()
        self._registration = context.register_service("probe", service)

    def stop(self, context):
        '''
        Bundle stopped
        '''
        if self._registration is not None:
            self._registration.unregister()
            self._registration = None