class DbscanModel(object):
    def __init__(self, model):
        if not hasattr(model, 'labels_') or not hasattr(model, 'components_') or not hasattr(model, 'eps'):
            raise ValueError("Model must be a fitted sklearn.cluster.DBSCAN instance.")
        self.eps = model.eps
        self.core_samples = model.components_
        self.core_labels = model.labels_[model.core_sample_indices_]

    def predict(self, point):
        pt = np.asarray(point)
        dists = np.linalg.norm(self.core_samples - pt, axis=1)
        idx = np.argmin(dists)
        return int(self.core_labels[idx]) if dists[idx] <= self.eps else -1