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
        self.items = list(items)
        self.abort_on_error = abort_on_error

    def __getattr__(self, name):
        def spawning_method(*args, **kwargs):
            def call(item):
                method = getattr(item, name)
                return method(*args, **kwargs)
            
            threads = []
            for item in self.items:
                thread = greenthread.spawn(call, item)
                threads.append(thread)
            
            if self.abort_on_error:
                # Wait for any thread to complete or raise an exception
                try:
                    results = []
                    for thread in threads:
                        results.append(thread.wait())
                    return results
                except Exception:
                    # Kill all remaining threads
                    for thread in threads:
                        thread.kill()
                    raise
            else:
                # Wait for all threads to complete
                results = []
                for thread in threads:
                    results.append(thread.wait())
                return results
        
        return spawning_method