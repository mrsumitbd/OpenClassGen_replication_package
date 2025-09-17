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
        self._server = None

    def start(self):
        '''
        Creates and starts the Local Lambda Invoke service. This method will block until the service is stopped
        manually using an interrupt. After the service is started, callers can make HTTP requests to the endpoint
        to invoke the Lambda function and receive a response.

        NOTE: This is a blocking call that will not return until the thread is interrupted with SIGINT/SIGTERM
        '''
        invoke_ctx = self.lambda_invoke_context

        class _Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                prefix = '/2015-03-31/functions/'
                suffix = '/invocations'
                path = self.path
                if not path.startswith(prefix) or not path.endswith(suffix):
                    self.send_error(404, 'Not Found')
                    return
                func_name = path[len(prefix):-len(suffix)]
                length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(length) if length > 0 else b''
                try:
                    event = json.loads(body.decode('utf-8')) if body else {}
                except Exception:
                    self.send_error(400, 'Invalid JSON')
                    return

                # Invoke the lambda locally
                result = invoke_ctx.invoke(func_name, event)
                # result may be tuple(status_code, headers_dict, body)
                if isinstance(result, tuple) and len(result) == 3:
                    status_code, headers, resp_body = result
                else:
                    # assume raw body return
                    status_code, headers, resp_body = 200, {}, result

                if not isinstance(resp_body, (bytes, bytearray)):
                    resp_body = json.dumps(resp_body).encode('utf-8')

                self.send_response(status_code)
                has_ct = False
                for k, v in headers.items():
                    self.send_header(k, v)
                    if k.lower() == 'content-type':
                        has_ct = True
                if not has_ct:
                    self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(resp_body)))
                self.end_headers()
                self.wfile.write(resp_body)

            def log_message(self, format, *args):
                return  # suppress default logging

        server = ThreadingHTTPServer((self.host, self.port), _Handler)
        if self.ssl_context:
            cert, key = self.ssl_context
            server.socket = ssl.wrap_socket(
                server.socket,
                certfile=cert,
                keyfile=key,
                server_side=True
            )
        self._server = server
        try:
            server.serve_forever()
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            server.server_close()