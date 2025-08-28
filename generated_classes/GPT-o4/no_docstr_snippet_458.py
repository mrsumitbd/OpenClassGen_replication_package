class PrintJustKeys(object):
    def __init__(self, out):
        self.out = out

    def next_record(self, record):
        line = ' '.join(str(k) for k in record.keys()) + '\n'
        self.out.write(line)