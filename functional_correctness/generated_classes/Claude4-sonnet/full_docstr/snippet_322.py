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
        
        if self.connection is None:
            self.connection = self.connection_pool.get_connection()
        
        try:
            for command in self.commands:
                self.connection.send_command(*command)
        except Exception as e:
            self.connection.disconnect()
            raise e

    def read(self):
        ''' '''
        if not self.commands:
            return []
        
        responses = []
        try:
            for _ in self.commands:
                response = self.connection.read_response()
                if self.parse_response:
                    response = self.parse_response(response)
                responses.append(response)
        except Exception as e:
            self.connection.disconnect()
            raise e
        finally:
            self.commands.clear()
            if self.connection:
                self.connection_pool.release(self.connection)
        
        return responses