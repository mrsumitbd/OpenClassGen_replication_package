class Client:
    ''' The client for the signal system, sending requests to the server.

    This implementation sends requests to a list stored in redis. Each request
    is implemented using the Request class and stored as a pickled object. The response
    from the server is stored under the unique response id.
    '''

    def __init__(self, connection, request_key):
        ''' Initialises the signal client.

        Args:
            connection: Reference to a signal connection object.
            request_key (str): The key under which the list of requests is stored.
        '''
        self.connection = connection
        self.request_key = request_key

    def send(self, request):
        ''' Send a request to the server and wait for its response.

        Args:
            request (Request): Reference to a request object that is sent to the server.

        Returns:
            Response: The response from the server to the request.
        '''
        pickled_request = pickle.dumps(request)
        self.connection.lpush(self.request_key, pickled_request)
        
        while True:
            response_data = self.connection.get(request.response_id)
            if response_data is not None:
                response = pickle.loads(response_data)
                self.connection.delete(request.response_id)
                return response
            time.sleep(0.01)