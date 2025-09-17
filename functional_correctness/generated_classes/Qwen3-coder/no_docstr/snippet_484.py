class LogStreamingServer:
    def __init__(self) -> None:
        self.server = None
        self.server_thread = None
        self.is_running = False
        self.log_queue = queue.Queue()
        self.clients = []

    @staticmethod
    def _get_free_port(spark_host_address: str = "") -> int:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((spark_host_address or 'localhost', 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port

    def start(self, spark_host_address: str = "") -> None:
        if self.is_running:
            return
            
        port = self._get_free_port(spark_host_address)
        self.is_running = True
        
        def serve_task(port: int) -> None:
            class LogHandler(BaseHTTPRequestHandler):
                def do_GET(self):
                    if self.path == '/logs':
                        self.send_response(200)
                        self.send_header('Content-Type', 'text/plain')
                        self.send_header('Cache-Control', 'no-cache')
                        self.send_header('Connection', 'keep-alive')
                        self.end_headers()
                        
                        # Keep connection open and stream logs
                        try:
                            while self.server.server_instance.is_running:
                                try:
                                    log_entry = self.server.server_instance.log_queue.get(timeout=1)
                                    self.wfile.write(f"{log_entry}\n".encode('utf-8'))
                                    self.wfile.flush()
                                except queue.Empty:
                                    continue
                        except (BrokenPipeError, ConnectionResetError):
                            pass
                    
                    elif self.path == '/health':
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(b'{"status": "healthy"}')
                    
                    else:
                        self.send_response(404)
                        self.end_headers()
                
                def log_message(self, format, *args):
                    # Suppress default logging
                    pass
            
            try:
                server = HTTPServer((spark_host_address or 'localhost', port), LogHandler)
                server.server_instance = self
                self.server = server
                server.serve_forever()
            except Exception:
                pass
        
        self.server_thread = threading.Thread(target=serve_task, args=(port,), daemon=True)
        self.server_thread.start()
        
        # Wait for server to start
        while self.server is None:
            time.sleep(0.1)
        
        self.port = port

    def shutdown(self) -> None:
        if not self.is_running:
            return
            
        self.is_running = False
        if self.server:
            self.server.shutdown()
        if self.server_thread:
            self.server_thread.join(timeout=5)