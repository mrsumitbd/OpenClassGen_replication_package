class Store(object):
    def __init__(self, conf):
        self.conf = conf
        self.batch_data = []
        self.chromosomes = []
        self.batch_size = conf.get('batch_size', 100) if conf else 100
        self.storage_path = conf.get('storage_path', './data') if conf else './data'
        
    def batch_save(self):
        if not self.batch_data:
            return
        
        import os
        import json
        
        os.makedirs(self.storage_path, exist_ok=True)
        
        batch_file = os.path.join(self.storage_path, f'batch_{len(self.batch_data)}.json')
        with open(batch_file, 'w') as f:
            json.dump(self.batch_data, f, indent=2)
        
        self.batch_data.clear()
    
    def save_chros(self):
        if not self.chromosomes:
            return
            
        import os
        import pickle
        
        os.makedirs(self.storage_path, exist_ok=True)
        
        chros_file = os.path.join(self.storage_path, 'chromosomes.pkl')
        with open(chros_file, 'wb') as f:
            pickle.dump(self.chromosomes, f)