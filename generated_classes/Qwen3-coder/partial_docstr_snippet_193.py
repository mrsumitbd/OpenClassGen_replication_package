class BetaStreamCollectorServicer(object):
    '''The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This class was generated
    only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0.'''


    def StreamMetrics(self, request_iterator, context):
        raise NotImplementedError()


    def GetMetricTypes(self, request, context):
        raise NotImplementedError()


    def Ping(self, request, context):
        raise NotImplementedError()


    def Kill(self, request, context):
        raise NotImplementedError()


    def GetConfigPolicy(self, request, context):
        raise NotImplementedError()