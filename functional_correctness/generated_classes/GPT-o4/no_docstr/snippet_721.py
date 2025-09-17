class Progress(object):

    def write_update(self, total, amount):
        if total <= 0:
            return
        percent = float(amount) / total * 100
        sys.stdout.write("\rProgress: {}/{} ({:.2f}%)".format(amount, total, percent))
        sys.stdout.flush()
        if amount >= total:
            sys.stdout.write("\n")
            sys.stdout.flush()

    def progress_pycurl(self, total, amount, _uploadtotal, _uploadamount):
        # Download progress
        if total and total > 0:
            self.write_update(total, amount)
        # Upload progress
        if _uploadtotal and _uploadtotal > 0:
            self.write_update(_uploadtotal, _uploadamount)
        return 0