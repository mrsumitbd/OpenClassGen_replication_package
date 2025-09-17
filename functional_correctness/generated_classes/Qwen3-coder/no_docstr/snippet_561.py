class Recorder:
    def __init__(self, rate=8000, chunksize=128):
        self.rate = rate
        self.chunksize = chunksize
        self.frames = []
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.recording = False
        self.lock = threading.Lock()

    def new_frame(self, data, frame_count, time_info, status):
        with self.lock:
            if self.recording:
                self.frames.append(data)
        return (data, pyaudio.paContinue)

    def get_frames(self):
        with self.lock:
            return self.frames.copy()

    def start(self):
        if not self.recording:
            self.frames = []
            self.stream = self.p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunksize,
                stream_callback=self.new_frame
            )
            self.recording = True
            self.stream.start_stream()

    def close(self):
        if self.recording and self.stream:
            self.recording = False
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()