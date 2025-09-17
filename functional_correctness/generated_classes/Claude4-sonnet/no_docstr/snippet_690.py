class DatasetLoop:
    def __init__(self, datasets, reader):
        self.datasets = datasets
        self.reader = reader
        self.current_index = 0

    def __repr__(self):
        return f"DatasetLoop(datasets={self.datasets}, reader={self.reader})"

    def __call__(self):
        while True:
            dataset = self.datasets[self.current_index]
            yield self.reader(dataset)
            self.current_index = (self.current_index + 1) % len(self.datasets)