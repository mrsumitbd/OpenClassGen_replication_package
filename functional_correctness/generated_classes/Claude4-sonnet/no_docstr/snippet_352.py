class DbscanModel(object):

    def __init__(self, model):
        self.model = model
        self.core_samples_ = model.core_sample_indices_
        self.labels_ = model.labels_
        self.X_ = model.components_
        self.eps = model.eps
        self.min_samples = model.min_samples
        self.nn = NearestNeighbors(radius=self.eps, metric=model.metric)
        self.nn.fit(self.X_)

    def predict(self, point):
        point = np.array(point).reshape(1, -1)
        neighbors = self.nn.radius_neighbors(point, return_distance=False)[0]
        
        if len(neighbors) == 0:
            return -1
        
        neighbor_labels = self.labels_[neighbors]
        neighbor_labels = neighbor_labels[neighbor_labels != -1]
        
        if len(neighbor_labels) == 0:
            return -1
        
        unique_labels, counts = np.unique(neighbor_labels, return_counts=True)
        return unique_labels[np.argmax(counts)]