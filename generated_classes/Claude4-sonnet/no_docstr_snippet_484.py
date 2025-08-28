class LogStreamingServer:
    def __init__(self) -> None:
        self.server: Optional[socketserver.TCPServer] = None
        self.server_thread: Optional[threading.Thread] = None
        self.port: Optional[int] = None

    @staticmethod
    def _get_free_port(spark_host_address: str = "") -> int:
        host = spark_host_address if spark_host_address else "localhost"
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port

    def start(self, spark_host_address: str = "") -> None:
        if self.server is not None:
            return
        
        host = spark_host_address if spark_host_address else "localhost"
        self.port = self._get_free_port(spark_host_address)
        
        class LogHandler(socketserver.StreamRequestHandler):
            def handle(self):
                while True:
                    try:
                        data = self.rfile.readline()
                        if not data:
                            break
                        sys.stdout.write(data.decode('utf-8'))
                        sys.stdout.flush()
                    except Exception:
                        break

        def serve_task(port: int) -> None:
            self.server = socketserver.TCPServer((host, port), LogHandler)
            self.server.serve_forever()

        self.server_thread = threading.Thread(target=serve_task, args=(self.port,))
        self.server_thread.daemon = True
        self.server_thread.start()

    def shutdown(self) -> None:
        if self.server is not None:
            self.server.shutdown()
            self.server.server_close()
            self.server = None
        if self.server_thread is not None:
            self.server_thread.join()
            self.server_thread = None
        self.port = None