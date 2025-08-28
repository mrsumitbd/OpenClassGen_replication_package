class BaseStreamComponent:
    '''
    The Base class for Stream Components.
    '''

    def __init__(self, handler_function, args=[]):
        '''
        :param handler_function: The function to execute on each message
        :param args: command line options or list representing as sys.argv
        '''
        self.handler_function = handler_function
        self.args = args
        self.running = False
        self.message_queue = Queue()
        self.worker_thread = None

    def start(self):
        '''
        Start the server and run forever.
        '''
        self.running = True
        self.worker_thread = threading.Thread(target=self._process_messages)
        self.worker_thread.daemon = True
        self.worker_thread.start()
        
        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.running = False
        if self.worker_thread:
            self.worker_thread.join()

    def _process_messages(self):
        while self.running:
            try:
                message = self.message_queue.get(timeout=0.1)
                if message is not None:
                    self.handler_function(message)
                self.message_queue.task_done()
            except Empty:
                continue

    def send_message(self, message):
        if self.running:
            self.message_queue.put(message)