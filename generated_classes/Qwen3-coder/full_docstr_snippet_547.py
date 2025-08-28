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
        self.streams = []

    def addStream(self, stream, t1=None, t2=None, limit=None, i1=None, i2=None, transform=None):
        '''Adds the given stream to the query construction. The function supports both stream
        names and Stream objects.'''
        stream_spec = {
            'stream': stream,
            't1': t1,
            't2': t2,
            'limit': limit,
            'i1': i1,
            'i2': i2,
            'transform': transform
        }
        self.streams.append(stream_spec)

    def run(self):
        '''Runs the merge query, and returns the result'''
        all_data = []
        
        for stream_spec in self.streams:
            stream = stream_spec['stream']
            t1 = stream_spec['t1']
            t2 = stream_spec['t2']
            limit = stream_spec['limit']
            i1 = stream_spec['i1']
            i2 = stream_spec['i2']
            transform = stream_spec['transform']
            
            # Handle both stream names and Stream objects
            if isinstance(stream, str):
                # Assume stream is a name and fetch from cdb
                stream_data = self.cdb.read(stream, t1=t1, t2=t2, limit=limit, i1=i1, i2=i2)
            else:
                # Assume stream is a Stream object
                stream_data = stream.read(t1=t1, t2=t2, limit=limit, i1=i1, i2=i2)
            
            # Apply transform if provided
            if transform and callable(transform):
                stream_data = transform(stream_data)
            
            all_data.extend(stream_data)
        
        # Sort by timestamp
        all_data.sort(key=lambda x: x['t'] if isinstance(x, dict) and 't' in x else getattr(x, 't', 0))
        
        return all_data