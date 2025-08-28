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
        # Serialize and enqueue the request
        payload = pickle.dumps(request)
        self.connection.rpush(self.request_key, payload)

        # Wait for the server to write the response under request.response_id
        response_key = request.response_id
        while not self.connection.exists(response_key):
            time.sleep(0.01)

        # Retrieve, deserialize, and clean up
        raw = self.connection.get(response_key)
        self.connection.delete(response_key)
        return pickle.loads(raw)