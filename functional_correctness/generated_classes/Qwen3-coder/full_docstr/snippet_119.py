class FileDownloader:
    '''Class for downloading files'''

    def __init__(self, url: str, dest_dir=None):
        '''Initialize a FileDownloader object
        * INPUTs:
          * url: File to download (full url)
                 (Ex. 'https://github.com/FPGAwars/apio-examples/
                       releases/download/0.0.35/apio-examples-0.0.35.zip')
          * dest_dir: Destination folder (where to download the file)
        '''
        self.url = url
        self.dest_dir = dest_dir
        self.response = None
        self.size = 0
        
        if self.dest_dir is None:
            self.dest_dir = os.getcwd()
        else:
            os.makedirs(self.dest_dir, exist_ok=True)
            
        # Extract filename from URL
        parsed_url = urlparse(url)
        self.filename = os.path.basename(parsed_url.path)
        if not self.filename:
            self.filename = 'downloaded_file'
        self.filepath = os.path.join(self.dest_dir, self.filename)

    def get_size(self) -> int:
        '''Return the size (in bytes) of the latest bytes block received'''
        return self.size

    def start(self):
        '''Start the downloading of the file'''
        self.response = requests.get(self.url, stream=True)
        self.response.raise_for_status()
        
        with open(self.filepath, 'wb') as f:
            for chunk in self.response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    self.size = len(chunk)

    def __del__(self):
        '''Close any pending request'''
        if hasattr(self, 'response') and self.response is not None:
            self.response.close()