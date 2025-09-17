class Progress(object):
    def write_update(self, total, amount):
        if total > 0:
            percent = (amount / total) * 100
            print(f"\rProgress: {percent:.1f}% ({amount}/{total})", end='', flush=True)
        else:
            print(f"\rProgress: {amount} bytes", end='', flush=True)

    def progress_pycurl(self, total, amount, _uploadtotal, _uploadamount):
        self.write_update(total, amount)