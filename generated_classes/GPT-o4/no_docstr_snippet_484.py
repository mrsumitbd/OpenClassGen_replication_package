class LogStreamingServer:
    def __init__(self) -> None:
        self._server_socket: socket.socket = None  # type: ignore
        self._serve_thread: threading.Thread = None  # type: ignore
        self._client_threads: list[threading.Thread] = []
        self._running = False
        self._port: int = 0

    @staticmethod
    def _get_free_port(spark_host_address: str = "") -> int:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            return s.getsockname()[1]

    def start(self, spark_host_address: str = "") -> None:
        host, port = ("localhost", 4040)
        if spark_host_address:
            if ":" in spark_host_address:
                h, p = spark_host_address.split(":", 1)
                host = h or host
                try:
                    port = int(p)
                except ValueError:
                    port = port
            else:
                host = spark_host_address
        self._port = self._get_free_port()
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind(('', self._port))
        self._server_socket.listen(5)
        self._server_socket.settimeout(1.0)
        self._running = True

        def serve_task(port: int) -> None:
            def forward(src: socket.socket, dst: socket.socket) -> None:
                try:
                    while True:
                        data = src.recv(4096)
                        if not data:
                            break
                        dst.sendall(data)
                except Exception:
                    pass
                finally:
                    try:
                        src.shutdown(socket.SHUT_RD)
                    except Exception:
                        pass
                    try:
                        dst.shutdown(socket.SHUT_WR)
                    except Exception:
                        pass

            while self._running:
                try:
                    client_sock, _ = self._server_socket.accept()
                except socket.timeout:
                    continue
                except OSError:
                    break
                try:
                    remote_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    remote_sock.connect((host, port))
                except Exception:
                    client_sock.close()
                    continue
                t1 = threading.Thread(target=forward, args=(client_sock, remote_sock))
                t2 = threading.Thread(target=forward, args=(remote_sock, client_sock))
                t1.daemon = True
                t2.daemon = True
                t1.start()
                t2.start()
                self._client_threads.extend([t1, t2])

        self._serve_thread = threading.Thread(target=serve_task, args=(port,))
        self._serve_thread.daemon = True
        self._serve_thread.start()

    def shutdown(self) -> None:
        self._running = False
        try:
            if self._server_socket:
                self._server_socket.close()
        except Exception:
            pass
        if self._serve_thread:
            self._serve_thread.join()
        for t in self._client_threads:
            t.join()