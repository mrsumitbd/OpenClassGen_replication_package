class Progress(object):
    def __init__(self):
        self.last_percent = -1

    def write_update(self, total, amount):
        if total == 0:
            return
        
        percent = int((amount * 100) / total)
        if percent != self.last_percent:
            self.last_percent = percent
            print(f"\rProgress: {percent}% ({amount}/{total})", end="", flush=True)
            if percent == 100:
                print()

    def progress_pycurl(self, total, amount, _uploadtotal, _uploadamount):
        self.write_update(total, amount)