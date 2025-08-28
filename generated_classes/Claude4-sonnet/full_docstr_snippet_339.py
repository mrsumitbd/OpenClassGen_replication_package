class RedisInfo:
    '''Class that establishes connection to Memcached Instance
    to retrieve statistics on operation.

    '''

    def __init__(self, host=None, port=None, db=None, password=None, 
                 socket_timeout=None, unix_socket_path=None):
        '''Initialize connection to Redis.
        
        @param host:             Redis Host.  (Default: localhost)
        @param port:             Redis Port.  (Default: Default Redis Port)
        @param db:               Redis DB ID. (Default: 0)
        @param password:         Redis Password (Optional)
        @param socket_timeout:   Redis Socket Timeout (Default: OS Default.)
        @param unix_socket_path: Socket File Path for UNIX Socket connections.
                                 (Not required unless connection to Redis is 
                                 through named socket.)
        
        '''
        self.host = host or 'localhost'
        self.port = port or 6379
        self.db = db or 0
        self.password = password
        self.socket_timeout = socket_timeout
        self.unix_socket_path = unix_socket_path
        
        if unix_socket_path:
            self.redis_client = redis.Redis(
                unix_socket_path=unix_socket_path,
                db=self.db,
                password=self.password,
                socket_timeout=self.socket_timeout
            )
        else:
            self.redis_client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                socket_timeout=self.socket_timeout
            )

    def ping(self):
        '''Ping Redis Server and return Round-Trip-Time in seconds.
        
        @return: Round-trip-time in seconds as float.
        
        '''
        start_time = time.time()
        self.redis_client.ping()
        end_time = time.time()
        return end_time - start_time

    def getStats(self):
        '''Query Redis and return stats.
        
        @return: Dictionary of stats.
        
        '''
        return self.redis_client.info()