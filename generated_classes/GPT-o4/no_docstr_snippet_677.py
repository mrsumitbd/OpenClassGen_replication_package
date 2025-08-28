class Progress(object):
    def __init__(self, output, length, **kwargs):
        self.output = output
        self.total = length
        self.bar_length = kwargs.get('bar_length', 50)
        self.fill_char = kwargs.get('fill_char', '#')
        self.empty_char = kwargs.get('empty_char', '-')
        self.prefix = kwargs.get('prefix', '')
        self.suffix = kwargs.get('suffix', '')
        self.decimals = kwargs.get('decimals', 1)
        self.end = kwargs.get('end', '\r')

    def get_percentage(self, current):
        if self.total == 0:
            return 100.0
        pct = (current / self.total) * 100
        return round(pct, self.decimals)

    def get_progress(self, current):
        pct = self.get_percentage(current)
        filled_len = int(self.bar_length * current / float(self.total or 1))
        bar = self.fill_char * filled_len + self.empty_char * (self.bar_length - filled_len)
        return f"{self.prefix}[{bar}]{pct}%{self.suffix}"

    def update(self, current):
        line = self.get_progress(current) + self.end
        self.output.write(line)
        self.output.flush()
        if current >= self.total:
            self.output.write('\n')
            self.output.flush()