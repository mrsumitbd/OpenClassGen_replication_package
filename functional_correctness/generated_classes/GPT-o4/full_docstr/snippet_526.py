class _BundleActivator(object):
    '''
    Bundle activator: registers a dummy probe service
    '''

    class _DummyProbeService(object):
        def probe(self):
            # Dummy implementation
            return "Probe OK"

    def __init__(self):
        '''
        Sets up members
        '''
        self._service = None
        self._registration = None

    def start(self, context):
        '''
        Bundle started
        '''
        # Instantiate and register the dummy probe service
        self._service = _BundleActivator._DummyProbeService()
        # The interface name can be any agreed-upon string
        interface = 'dummy.probe.service'
        properties = {}
        self._registration = context.register_service(interface,
                                                      self._service,
                                                      properties)

    def stop(self, context):
        '''
        Bundle stopped
        '''
        # Unregister the service if it was registered
        if self._registration:
            try:
                context.unregister_service(self._registration)
            except Exception:
                pass
            finally:
                self._registration = None
                self._service = None