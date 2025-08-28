class Recorder:
    def __init__(self, rate=8000, chunksize=128):
        self.rate = rate
        self.chunksize = chunksize
        self.frames = []
        self.pa = None
        self.stream = None

    def new_frame(self, data, frame_count, time_info, status):
        # data is bytes
        self.frames.append(data)
        return (None, pyaudio.paContinue)

    def get_frames(self):
        return b''.join(self.frames)

    def start(self):
        if self.stream is not None:
            return
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunksize,
            stream_callback=self.new_frame
        )
        self.stream.start_stream()

    def close(self):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        if self.pa is not None:
            self.pa.terminate()
            self.pa = None