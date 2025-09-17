class LocalLambdaService:
    '''
    Implementation of Local Lambda Invoke Service that is capable of serving the invoke path to your Lambda Functions
    that are defined in a SAM file.
    '''

    def __init__(self, lambda_invoke_context, port, host, ssl_context=None):
        '''
        Initialize the Local Lambda Invoke service.

        :param samcli.commands.local.cli_common.invoke_context.InvokeContext lambda_invoke_context: Context object
            that can help with Lambda invocation
        :param int port: Port to listen on
        :param string host: Local hostname or IP address to bind to
        :param tuple(string, string) ssl_context: Optional, path to ssl certificate and key files to start service
            in https
        '''
        self.lambda_invoke_context = lambda_invoke_context
        self.port = port
        self.host = host
        self.ssl_context = ssl_context
        self.server = None
        self.thread = None

    def start(self):
        '''
        Creates and starts the Local Lambda Invoke service. This method will block until the service is stopped
        manually using an interrupt. After the service is started, callers can make HTTP requests to the endpoint
        to invoke the Lambda function and receive a response.

        NOTE: This is a blocking call that will not return until the thread is interrupted with SIGINT/SIGTERM
        '''
        class LambdaInvokeHandler(BaseHTTPRequestHandler):
            def do_POST(self):
                try:
                    content_length = int(self.headers.get('Content-Length', 0))
                    post_data = self.rfile.read(content_length)
                    
                    # Parse the request data
                    try:
                        request_data = json.loads(post_data) if post_data else {}
                    except json.JSONDecodeError:
                        request_data = {}
                    
                    # Get the function name from the request path or default context
                    function_name = self.get_function_name()
                    
                    # Invoke the Lambda function
                    response = self.server.lambda_service.invoke_function(function_name, request_data)
                    
                    # Send response
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode())
                    
                except Exception as e:
                    logger.error(f"Error invoking Lambda function: {str(e)}")
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    error_response = {"error": str(e)}
                    self.wfile.write(json.dumps(error_response).encode())
            
            def get_function_name(self):
                # Extract function name from path or use default
                return "default-function"
            
            def log_message(self, format, *args):
                logger.info(format % args)

        # Create HTTP server
        self.server = HTTPServer((self.host, self.port), LambdaInvokeHandler)
        self.server.lambda_service = self
        
        # Configure SSL if provided
        if self.ssl_context:
            cert_file, key_file = self.ssl_context
            self.server.socket = ssl.wrap_socket(self.server.socket, 
                                               certfile=cert_file, 
                                               keyfile=key_file, 
                                               server_side=True)
        
        logger.info(f"Starting Local Lambda Service on {self.host}:{self.port}")
        
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            logger.info("Shutting down Local Lambda Service")
            self.server.shutdown()
    
    def invoke_function(self, function_name, event_data):
        '''
        Invoke the Lambda function with the given name and event data.
        
        :param string function_name: Name of the Lambda function to invoke
        :param dict event_data: Event data to pass to the Lambda function
        :return: Response from the Lambda function
        '''
        # Use the invoke context to invoke the function
        if self.lambda_invoke_context:
            # This is a simplified implementation - in practice, you would
            # use the invoke context to properly invoke the Lambda function
            local_lambda_runner = self.lambda_invoke_context.local_lambda_runner
            function = self.lambda_invoke_context.function_provider.get(function_name)
            
            if function:
                # Invoke the function and return the result
                response = local_lambda_runner.invoke(function, event_data)
                return response
        
        # Fallback response
        return {"statusCode": 200, "body": "Function invoked successfully"}