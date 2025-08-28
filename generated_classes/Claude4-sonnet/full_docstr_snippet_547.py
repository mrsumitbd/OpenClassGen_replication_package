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
        stream_info = {
            'stream': stream,
            't1': t1,
            't2': t2,
            'limit': limit,
            'i1': i1,
            'i2': i2,
            'transform': transform
        }
        self.streams.append(stream_info)

    def run(self):
        '''Runs the merge query, and returns the result'''
        all_data = []
        
        for stream_info in self.streams:
            stream = stream_info['stream']
            if isinstance(stream, str):
                stream_obj = self.cdb[stream]
            else:
                stream_obj = stream
            
            params = {}
            for key in ['t1', 't2', 'limit', 'i1', 'i2', 'transform']:
                if stream_info[key] is not None:
                    params[key] = stream_info[key]
            
            data = stream_obj.read(**params)
            all_data.extend(data)
        
        all_data.sort(key=lambda x: x['t'])
        return all_data