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
        
        if client is not None:
            self.client = client
        else:
            from raven import Client
            self.client = Client(**kwargs)

    def server_inspect_exception(self, req_event, rep_event, task_ctx, exc_info):
        '''
        Called when an exception has been raised in the code run by ZeroRPC
        '''
        exc_type, exc_value, exc_traceback = exc_info
        
        if self.hide_zerorpc_frames:
            # Filter out zerorpc frames from the traceback
            import traceback
            tb_list = traceback.extract_tb(exc_traceback)
            filtered_tb_list = [frame for frame in tb_list if 'zerorpc' not in frame.filename]
            
            if filtered_tb_list:
                # Create a new traceback with filtered frames
                import sys
                exc_traceback = None
                for frame in reversed(filtered_tb_list):
                    exc_traceback = traceback.FrameSummary(
                        frame.filename, frame.lineno, frame.name, frame.line
                    )
        
        # Capture the exception with Raven client
        self.client.captureException(exc_info=(exc_type, exc_value, exc_traceback))