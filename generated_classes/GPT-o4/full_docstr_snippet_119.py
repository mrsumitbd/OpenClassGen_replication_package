class FileDownloader:
    '''Class for downloading files'''

    def __init__(self, url: str, dest_dir=None):
        '''Initialize a FileDownloader object
            * INPUTs:
              * url: File to download (full url)
              * dest_dir: Destination folder
        '''
        self.url = url
        self.dest_dir = dest_dir or os.getcwd()
        if not os.path.isdir(self.dest_dir):
            os.makedirs(self.dest_dir, exist_ok=True)
        self.filename = os.path.basename(self.url)
        self.filepath = os.path.join(self.dest_dir, self.filename)
        self._last_block_size = 0
        self._response = None

    def get_size(self) -> int:
        '''Return the size (in bytes) of the latest bytes block received'''
        return self._last_block_size

    def start(self):
        '''Start the downloading of the file'''
        try:
            self._response = urlopen(self.url)
            with open(self.filepath, 'wb') as f:
                while True:
                    chunk = self._response.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
                    self._last_block_size = len(chunk)
        except (HTTPError, URLError) as e:
            raise RuntimeError(f"Download failed: {e}")
        finally:
            if self._response:
                try:
                    self._response.close()
                except:
                    pass
                self._response = None

    def __del__(self):
        '''Close any pending request'''
        if self._response:
            try:
                self._response.close()
            except:
                pass
            self._response = None