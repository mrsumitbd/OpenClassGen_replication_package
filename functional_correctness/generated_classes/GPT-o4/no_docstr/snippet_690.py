class DatasetLoop:
    def __init__(self, datasets, reader):
        """
        datasets: iterable of dataset identifiers (e.g., filenames or objects)
        reader: callable taking one dataset identifier and returning an iterable of records
        """
        if not hasattr(datasets, "__iter__"):
            raise TypeError("datasets must be an iterable")
        if not callable(reader):
            raise TypeError("reader must be callable")
        self.datasets = list(datasets)
        self.reader = reader

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"datasets={self.datasets!r}, "
            f"reader={self.reader!r}"
            f")"
        )

    def __call__(self):
        for ds in self.datasets:
            for record in self.reader(ds):
                yield record