class Store(object):
    def __init__(self, conf):
        self.conf = conf
        self.data = []

    def batch_save(self):
        # Save all data in batch
        if self.data:
            # Simulate saving data
            saved_count = len(self.data)
            self.data = []
            return saved_count
        return 0

    def save_chros(self):
        # Save chromosome data
        return self.batch_save()