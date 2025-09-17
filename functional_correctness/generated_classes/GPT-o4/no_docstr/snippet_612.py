class Store(object):

    def __init__(self, conf):
        self.conf = conf.copy() if isinstance(conf, dict) else {}
        self.batch_file = self.conf.get('batch_file', 'batch.jsonl')
        self.chros_file = self.conf.get('chros_file', 'chros.json')
        self.batch_size = self.conf.get('batch_size', 1000)
        bp = os.path.dirname(self.batch_file) or '.'
        cp = os.path.dirname(self.chros_file) or '.'
        os.makedirs(bp, exist_ok=True)
        os.makedirs(cp, exist_ok=True)
        self._batch = []
        self._chros = []

    def batch_save(self, item):
        self._batch.append(item)
        if len(self._batch) >= self.batch_size:
            self._flush_batch()

    def save_chros(self):
        with open(self.chros_file, 'w') as f:
            json.dump(self._chros, f, indent=2)

    def _flush_batch(self):
        with open(self.batch_file, 'a') as f:
            for record in self._batch:
                f.write(json.dumps(record) + "\n")
        self._batch = []