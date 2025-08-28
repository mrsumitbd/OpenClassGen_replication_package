class NodeCommands:
    ''' '''

    def __init__(self, parse_response, connection_pool, connection):
        ''' '''
        self.parse_response = parse_response
        self.connection_pool = connection_pool
        self.connection = connection
        self.commands = []

    def append(self, c):
        ''' '''
        self.commands.append(c)

    def write(self):
        '''
        Code borrowed from Redis so it can be fixed
        '''
        if not self.commands:
            return
        
        # Get a connection from the pool if we don't have one
        connection = self.connection or self.connection_pool.get_connection()
        
        try:
            # Write all commands to the connection
            for command in self.commands:
                connection.send_command(*command)
        except Exception:
            # If there's an error, make sure to release the connection
            if not self.connection:
                self.connection_pool.release(connection)
            raise
        
        # If we're using a connection from the pool, release it
        if not self.connection:
            self.connection_pool.release(connection)

    def read(self):
        ''' '''
        if not self.commands:
            return []
        
        results = []
        # Get a connection from the pool if we don't have one
        connection = self.connection or self.connection_pool.get_connection()
        
        try:
            # Read responses for all commands
            for _ in self.commands:
                response = connection.read_response()
                if self.parse_response:
                    response = self.parse_response(response)
                results.append(response)
        finally:
            # If we're using a connection from the pool, release it
            if not self.connection:
                self.connection_pool.release(connection)
        
        return results