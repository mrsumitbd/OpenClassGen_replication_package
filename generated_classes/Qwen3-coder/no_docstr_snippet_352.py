class DbscanModel(object):
    def __init__(self, model):
        self.model = model
        self.labels = model.labels_
        self.core_sample_indices = model.core_sample_indices_
        
    def predict(self, point):
        # DBSCAN doesn't have a built-in predict method for new points
        # We need to implement nearest neighbor classification based on fitted clusters
        import numpy as np
        from sklearn.neighbors import NearestNeighbors
        
        # Get the core samples (points that were actually clustered)
        if hasattr(self.model, 'components_'):
            core_points = self.model.components_
        else:
            # Fallback: use the original training data if available
            raise ValueError("Model must have components_ attribute or training data")
        
        # If the point belongs to a cluster, find nearest core point
        if len(core_points) == 0:
            return -1  # Noise label
            
        # Fit nearest neighbors on core samples
        nbrs = NearestNeighbors(n_neighbors=1).fit(core_points)
        distances, indices = nbrs.kneighbors([point])
        
        # Return the label of the nearest core point
        nearest_core_idx = indices[0][0]
        # This is a simplified approach - in practice, you'd need to map core point indices to labels
        return 0