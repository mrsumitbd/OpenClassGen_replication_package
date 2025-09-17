class CSVReporter(object):

    def __init__(self, directory):
        self.directory = directory
        os.makedirs(self.directory, exist_ok=True)
        self._headers = {
            'histogram': ['timestamp', 'count', 'min', 'max', 'mean', 'stddev',
                          'p50', 'p75', 'p95', 'p98', 'p99', 'p999'],
            'meter': ['timestamp', 'count', 'mean_rate', 'm1_rate', 'm5_rate', 'm15_rate']
        }

    def file_name(self, name, kind):
        fname = f"{name}-{kind}.csv"
        return os.path.join(self.directory, fname)

    def dump_histogram(self, name, obj):
        fn = self.file_name(name, 'histogram')
        is_new = not os.path.exists(fn)
        with open(fn, 'a', newline='') as f:
            writer = csv.writer(f)
            if is_new:
                writer.writerow(self._headers['histogram'])
            ts = int(time.time())
            # expect obj to have count, min, max, mean, stddev and percentiles() -> dict
            cnt = getattr(obj, 'count', '')
            mn  = getattr(obj, 'min', '')
            mx  = getattr(obj, 'max', '')
            mean = getattr(obj, 'mean', '')
            std = getattr(obj, 'stddev', '')
            # percentiles: 50,75,95,98,99,99.9
            percs = {}
            if hasattr(obj, 'percentiles'):
                try:
                    percs = obj.percentiles()
                except:
                    percs = {}
            row = [
                ts, cnt, mn, mx, mean, std,
                percs.get(50, ''),
                percs.get(75, ''),
                percs.get(95, ''),
                percs.get(98, ''),
                percs.get(99, ''),
                percs.get(99.9, ''),
            ]
            writer.writerow(row)

    def dump_meter(self, name, obj):
        fn = self.file_name(name, 'meter')
        is_new = not os.path.exists(fn)
        with open(fn, 'a', newline='') as f:
            writer = csv.writer(f)
            if is_new:
                writer.writerow(self._headers['meter'])
            ts = int(time.time())
            cnt = getattr(obj, 'count', '')
            mean_rate = getattr(obj, 'mean_rate', '')
            m1 = getattr(obj, 'm1_rate', '')
            m5 = getattr(obj, 'm5_rate', '')
            m15 = getattr(obj, 'm15_rate', '')
            row = [ts, cnt, mean_rate, m1, m5, m15]
            writer.writerow(row)

    def __call__(self, objects):
        for name, obj in objects.items():
            # try histogram first
            try:
                self.dump_histogram(name, obj)
            except Exception:
                pass
            # then meter
            try:
                self.dump_meter(name, obj)
            except Exception:
                pass