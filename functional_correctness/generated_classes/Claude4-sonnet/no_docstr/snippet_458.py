class PrintJustKeys(object):

    def __init__(self, out):
        self.out = out

    def next_record(self, record):
        if isinstance(record, dict):
            for key in record.keys():
                self.out.write(str(key) + '\n')