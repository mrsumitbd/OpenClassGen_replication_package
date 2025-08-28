class Progress(object):
    def __init__(self, output, length, **kwargs):
        self.output = output
        self.length = length
        self.width = kwargs.get('width', 50)
        self.fill_char = kwargs.get('fill_char', '#')
        self.empty_char = kwargs.get('empty_char', '-')
        self.show_percentage = kwargs.get('show_percentage', True)
        
    def get_percentage(self, current):
        if self.length <= 0:
            return 100.0
        return (current / self.length) * 100
        
    def get_progress(self, current):
        if self.length <= 0:
            filled_length = self.width
        else:
            filled_length = int((current / self.length) * self.width)
        
        filled = self.fill_char * min(filled_length, self.width)
        empty = self.empty_char * max(0, self.width - filled_length)
        
        bar = f"[{filled}{empty}]"
        
        if self.show_percentage:
            percentage = self.get_percentage(current)
            bar += f" {percentage:.1f}%"
            
        return bar
        
    def update(self, current):
        progress_bar = self.get_progress(current)
        self.output.write(f"\r{progress_bar}")
        self.output.flush()