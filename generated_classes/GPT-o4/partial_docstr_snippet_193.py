class BetaStreamCollectorServicer(object):
    '''The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This class was generated
    only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0.'''

    def StreamMetrics(self, request_iterator, context):
        context.abort(
            grpc.StatusCode.UNIMPLEMENTED,
            'Beta API StreamMetrics is deprecated for 0.15.0 and later; use the GA API instead.'
        )

    def GetMetricTypes(self, request, context):
        context.abort(
            grpc.StatusCode.UNIMPLEMENTED,
            'Beta API GetMetricTypes is deprecated for 0.15.0 and later; use the GA API instead.'
        )

    def Ping(self, request, context):
        context.abort(
            grpc.StatusCode.UNIMPLEMENTED,
            'Beta API Ping is deprecated for 0.15.0 and later; use the GA API instead.'
        )

    def Kill(self, request, context):
        context.abort(
            grpc.StatusCode.UNIMPLEMENTED,
            'Beta API Kill is deprecated for 0.15.0 and later; use the GA API instead.'
        )

    def GetConfigPolicy(self, request, context):
        context.abort(
            grpc.StatusCode.UNIMPLEMENTED,
            'Beta API GetConfigPolicy is deprecated for 0.15.0 and later; use the GA API instead.'
        )