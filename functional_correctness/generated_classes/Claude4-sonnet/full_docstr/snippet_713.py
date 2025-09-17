class SentryMiddleware(object):
    '''Sentry/Raven middleware for ZeroRPC.

    >>> import zerorpc
    >>> from raven.contrib.zerorpc import SentryMiddleware
    >>> sentry = SentryMiddleware(dsn='udp://..../')
    >>> zerorpc.Context.get_instance().register_middleware(sentry)

    Exceptions detected server-side in ZeroRPC will be submitted to Sentry (and
    propagated to the client as well).
    '''

    def __init__(self, hide_zerorpc_frames=True, client=None, **kwargs):
        '''
        Create a middleware object that can be injected in a ZeroRPC server.

        - hide_zerorpc_frames: modify the exception stacktrace to remove the
                               internal zerorpc frames (True by default to make
                               the stacktrace as readable as possible);
        - client: use an existing raven.Client object, otherwise one will be
                  instantiated from the keyword arguments.
        '''
        self.hide_zerorpc_frames = hide_zerorpc_frames
        if client is None:
            from raven import Client
            self.client = Client(**kwargs)
        else:
            self.client = client

    def server_inspect_exception(self, req_event, rep_event, task_ctx, exc_info):
        '''
        Called when an exception has been raised in the code run by ZeroRPC
        '''
        if self.hide_zerorpc_frames:
            import traceback
            tb = exc_info[2]
            frames = []
            while tb is not None:
                frame = tb.tb_frame
                filename = frame.f_code.co_filename
                if not ('zerorpc' in filename and 'site-packages' in filename):
                    frames.append(tb)
                tb = tb.tb_next
            
            if frames:
                exc_info = (exc_info[0], exc_info[1], frames[-1])
        
        self.client.captureException(exc_info=exc_info, extra={
            'zerorpc_event': req_event.name if req_event else None,
            'zerorpc_args': req_event.args if req_event else None
        })