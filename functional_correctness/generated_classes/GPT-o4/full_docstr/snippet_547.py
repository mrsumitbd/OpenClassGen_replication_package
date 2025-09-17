class Merge(object):
    '''Merge represents a query which allows to merge multiple streams into one
    when reading, with all the streams merged together by increasing timestamp.
    The merge query is used as a constructor-type object::

        m = Merge(cdb)
        m.addStream("mystream1",t1=time.time()-10)
        m.addStream("mystream2",t1=time.time()-10)
        result = m.run()
    '''

    def __init__(self, cdb):
        '''Given a ConnectorDB object, begins the construction of a Merge query'''
        self.cdb = cdb
        self._streams = []

    def addStream(self, stream, t1=None, t2=None, limit=None,
                  i1=None, i2=None, transform=None):
        '''Adds the given stream to the query construction. The function supports both stream
        names and Stream objects.'''
        self._streams.append({
            'stream': stream,
            't1': t1,
            't2': t2,
            'limit': limit,
            'i1': i1,
            'i2': i2,
            'transform': transform
        })
        return self

    def run(self):
        '''Runs the merge query, and returns the result'''
        iterators = []

        for spec in self._streams:
            src = spec['stream']
            t1, t2 = spec['t1'], spec['t2']
            limit, i1, i2 = spec['limit'], spec['i1'], spec['i2']
            transform = spec['transform']

            # obtain a raw iterator of rows
            if isinstance(src, str):
                # assume cdb.get_stream returns an iterator of dicts with a 't' timestamp key
                rows = self.cdb.get_stream(src,
                                           t1=t1, t2=t2,
                                           limit=limit,
                                           i1=i1, i2=i2)
            elif hasattr(src, 'run') and callable(src.run):
                # assume it's another query object
                rows = src.run()
            else:
                raise TypeError("Stream must be a name or an object with run()")

            # apply transform if provided
            if transform is not None:
                rows = map(transform, rows)

            # wrap each row as (timestamp, row) for merging
            def wrapped(r_iter):
                for r in r_iter:
                    if 't' not in r:
                        raise KeyError("Each row must have a 't' timestamp field")
                    yield (r['t'], r)

            iterators.append(wrapped(rows))

        # merge all iterators by the timestamp key
        merged = heapq.merge(*iterators, key=lambda x: x[0])

        # return only the row dicts, in order
        return [row for (_, row) in merged]