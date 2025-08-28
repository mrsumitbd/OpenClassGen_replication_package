class CSVReporter(object):
    def __init__(self, directory):
        self.directory = directory
        if not os.path.exists(directory):
            os.makedirs(directory)

    def file_name(self, name, kind):
        return os.path.join(self.directory, f"{name}_{kind}.csv")

    def dump_histogram(self, name, obj):
        filename = self.file_name(name, 'histogram')
        file_exists = os.path.exists(filename)
        
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(['timestamp', 'count', 'min', 'max', 'mean', 'stddev'])
            
            timestamp = datetime.now().isoformat()
            row = [timestamp, obj.get('count', 0), obj.get('min', 0), obj.get('max', 0), 
                   obj.get('mean', 0), obj.get('stddev', 0)]
            writer.writerow(row)

    def dump_meter(self, name, obj):
        filename = self.file_name(name, 'meter')
        file_exists = os.path.exists(filename)
        
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(['timestamp', 'count', 'm1_rate', 'm5_rate', 'm15_rate', 'mean_rate'])
            
            timestamp = datetime.now().isoformat()
            row = [timestamp, obj.get('count', 0), obj.get('m1_rate', 0), obj.get('m5_rate', 0), 
                   obj.get('m15_rate', 0), obj.get('mean_rate', 0)]
            writer.writerow(row)

    def __call__(self, objects):
        for name, obj in objects.items():
            if 'histogram' in name.lower() or (isinstance(obj, dict) and 'count' in obj and 'mean' in obj):
                self.dump_histogram(name, obj)
            elif 'meter' in name.lower() or (isinstance(obj, dict) and 'm1_rate' in obj):
                self.dump_meter(name, obj)