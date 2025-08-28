class SpawningProxy(object):

    def __init__(self, items, abort_on_error=False):
        ''' Wraps an iterable set of items such that a call on the returned
            SpawningProxy instance will spawn a call in a
            :class:`~eventlet.greenthread.GreenThread` for each item.

            Returns when every spawned thread has completed.

            :param items: Iterable item set to process
            :param abort_on_error: If True, any exceptions raised on an individual
                item call will cause all peer item call threads to be killed, and
                for the exception to be propagated to the caller immediately.
            '''
        self.items = items
        self.abort_on_error = abort_on_error

    def __getattr__(self, name):
        def spawning_method(*args, **kwargs):
            threads = []
            results = []
            
            def call(item):
                method = getattr(item, name)
                return method(*args, **kwargs)
            
            for item in self.items:
                thread = eventlet.spawn(call, item)
                threads.append(thread)
            
            if self.abort_on_error:
                for thread in threads:
                    results.append(thread.wait())
            else:
                for thread in threads:
                    try:
                        results.append(thread.wait())
                    except Exception:
                        results.append(None)
            
            return results
        
        return spawning_method