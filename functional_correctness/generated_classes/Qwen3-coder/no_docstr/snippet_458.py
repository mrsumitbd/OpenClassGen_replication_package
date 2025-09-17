class PrintJustKeys(object):
    def __init__(self, out):
        self.out = out

    def next_record(self, record):
        if record is not None and len(record) > 0:
            key = record[0]
            self.out.write(str(key) + '\n')