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
        if client is not None:
            self.client = client
        else:
            self.client = Client(**kwargs)
        self.hide_zerorpc_frames = hide_zerorpc_frames

    def server_inspect_exception(self, req_event, rep_event, task_ctx, exc_info):
        '''
        Called when an exception has been raised in the code run by ZeroRPC
        '''
        etype, evalue, tb = exc_info
        if self.hide_zerorpc_frames:
            try:
                frames = []
                current = tb
                while current:
                    modname = current.tb_frame.f_globals.get('__name__', '')
                    if not modname.startswith('zerorpc'):
                        frames.append((current.tb_frame, current.tb_frame.f_lasti, current.tb_lineno))
                    current = current.tb_next
                new_tb = None
                for frame, lasti, lineno in reversed(frames):
                    new_tb = types.TracebackType(new_tb, frame, lasti, lineno)
                tb = new_tb
                exc_info = (etype, evalue, tb)
            except Exception:
                pass
        self.client.captureException(exc_info=exc_info)
        return None