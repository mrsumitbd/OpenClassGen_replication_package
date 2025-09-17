class CSVReporter(object):

    def __init__(self, directory):
        self.directory = directory
        if not os.path.exists(directory):
            os.makedirs(directory)

    def file_name(self, name, kind):
        return os.path.join(self.directory, f"{name}_{kind}.csv")

    def dump_histogram(self, name, obj):
        filename = self.file_name(name, "histogram")
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['bucket', 'count'])
            if hasattr(obj, 'buckets'):
                for bucket, count in obj.buckets.items():
                    writer.writerow([bucket, count])
            elif hasattr(obj, 'items'):
                for bucket, count in obj.items():
                    writer.writerow([bucket, count])

    def dump_meter(self, name, obj):
        filename = self.file_name(name, "meter")
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['metric', 'value'])
            if hasattr(obj, 'count'):
                writer.writerow(['count', obj.count])
            if hasattr(obj, 'rate'):
                writer.writerow(['rate', obj.rate])
            if hasattr(obj, 'mean_rate'):
                writer.writerow(['mean_rate', obj.mean_rate])
            if hasattr(obj, 'one_minute_rate'):
                writer.writerow(['one_minute_rate', obj.one_minute_rate])
            if hasattr(obj, 'five_minute_rate'):
                writer.writerow(['five_minute_rate', obj.five_minute_rate])
            if hasattr(obj, 'fifteen_minute_rate'):
                writer.writerow(['fifteen_minute_rate', obj.fifteen_minute_rate])

    def __call__(self, objects):
        for name, obj in objects.items():
            obj_type = type(obj).__name__.lower()
            if 'histogram' in obj_type or hasattr(obj, 'buckets'):
                self.dump_histogram(name, obj)
            elif 'meter' in obj_type or hasattr(obj, 'rate') or hasattr(obj, 'count'):
                self.dump_meter(name, obj)