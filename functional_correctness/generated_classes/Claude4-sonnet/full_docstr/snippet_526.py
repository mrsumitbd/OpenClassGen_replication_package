class _BundleActivator(object):
    '''
    Bundle activator: registers a dummy probe service
    '''

    def __init__(self):
        '''
        Sets up members
        '''
        self._registration = None
        self._service = None

    def start(self, context):
        '''
        Bundle started
        '''
        self._service = DummyProbeService()
        self._registration = context.register_service(
            "probe.service", self._service, {}
        )

    def stop(self, context):
        '''
        Bundle stopped
        '''
        if self._registration:
            self._registration.unregister()
            self._registration = None
        self._service = None