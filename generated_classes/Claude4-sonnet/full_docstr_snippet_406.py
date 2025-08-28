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
        self.app = Flask(__name__)
        self.server = None
        self._setup_routes()

    def _setup_routes(self):
        @self.app.route('/2015-03-31/functions/<function_name>/invocations', methods=['POST'])
        def invoke_function(function_name):
            try:
                payload = request.get_data()
                if not payload:
                    payload = b'{}'
                
                stdout, stderr = self.lambda_invoke_context.local_lambda_runner.invoke(
                    function_name,
                    payload,
                    stdout=None,
                    stderr=None
                )
                
                return stdout
            except Exception as e:
                return jsonify({'errorMessage': str(e), 'errorType': type(e).__name__}), 500

    def start(self):
        '''
        Creates and starts the Local Lambda Invoke service. This method will block until the service is stopped
        manually using an interrupt. After the service is started, callers can make HTTP requests to the endpoint
        to invoke the Lambda function and receive a response.

        NOTE: This is a blocking call that will not return until the thread is interrupted with SIGINT/SIGTERM
        '''
        self.server = make_server(
            self.host,
            self.port,
            self.app,
            ssl_context=self.ssl_context,
            threaded=True
        )
        
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.server.shutdown()