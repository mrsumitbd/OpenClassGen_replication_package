class Progress(object):
    def __init__(self, output, length, **kwargs):
        self.output = output
        self.length = length
        self.current = 0
        self.last_output = ""
        
    def get_percentage(self, current):
        if self.length == 0:
            return 0
        return min(100, max(0, (current / self.length) * 100))
    
    def get_progress(self, current):
        percentage = self.get_percentage(current)
        return f"Progress: {current}/{self.length} ({percentage:.1f}%)"
    
    def update(self, current):
        self.current = current
        progress_str = self.get_progress(current)
        
        # Clear previous output
        if self.last_output:
            self.output.write('\r' + ' ' * len(self.last_output) + '\r')
        
        # Write new progress
        self.output.write(progress_str)
        self.output.flush()
        
        self.last_output = progress_str