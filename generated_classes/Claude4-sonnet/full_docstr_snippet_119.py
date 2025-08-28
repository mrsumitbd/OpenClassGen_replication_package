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
        self.dest_dir = dest_dir if dest_dir else os.getcwd()
        self.response = None
        self.latest_chunk_size = 0
        
        # Extract filename from URL
        parsed_url = urlparse(url)
        self.filename = os.path.basename(parsed_url.path)
        if not self.filename:
            self.filename = 'downloaded_file'
        
        self.dest_path = os.path.join(self.dest_dir, self.filename)

    def get_size(self) -> int:
        '''Return the size (in bytes) of the latest bytes block received'''
        return self.latest_chunk_size

    def start(self):
        '''Start the downloading of the file'''
        try:
            self.response = requests.get(self.url, stream=True)
            self.response.raise_for_status()
            
            # Create destination directory if it doesn't exist
            os.makedirs(self.dest_dir, exist_ok=True)
            
            with open(self.dest_path, 'wb') as file:
                for chunk in self.response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        self.latest_chunk_size = len(chunk)
                        
        except Exception as e:
            if self.response:
                self.response.close()
                self.response = None
            raise e

    def __del__(self):
        '''Close any pending request'''
        if hasattr(self, 'response') and self.response:
            self.response.close()