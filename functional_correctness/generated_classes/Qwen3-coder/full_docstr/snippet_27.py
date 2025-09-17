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
        # Generate a unique response ID
        response_id = str(uuid.uuid4())
        request.response_id = response_id
        
        # Pickle the request object
        pickled_request = pickle.dumps(request)
        
        # Push the request to the Redis list
        self.connection.lpush(self.request_key, pickled_request)
        
        # Wait for the response
        response_key = f"response:{response_id}"
        pickled_response = self.connection.brpoplpush(response_key, response_key, timeout=30)
        
        # Unpickle and return the response
        response = pickle.loads(pickled_response)
        
        # Clean up the response key
        self.connection.delete(response_key)
        
        return response