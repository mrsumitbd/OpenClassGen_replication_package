class Zoom3D(object):
    '''
    Create an ANTs Affine Transform with a specified level
    of zoom. Any value greater than 1 implies a "zoom-out" and anything
    less than 1 implies a "zoom-in".
    '''

    def __init__(self, zoom, reference=None, lazy=False):
        '''
        Initialize a Zoom3D object

        Arguments
        ---------
        zoom : list or tuple
            Lower and Upper bounds on zoom parameter.
            e.g. zoom_range = (0.7,0.9) will result in a random
            draw of the zoom parameters between 0.7 and 0.9

        reference : ANTsImage (optional but recommended)
            image providing the reference space for the transform.
            this will also set the transform fixed parameters.

        lazy : boolean (default = False)
            if True, calling the `transform` method only returns
            the randomly generated transform and does not actually
            transform the image
        '''
        self.zoom = zoom
        self.reference = reference
        self.lazy = lazy
        self.transform_ = None

    def transform(self, X=None, y=None):
        '''
        Transform an image using an Affine transform with the given
        zoom parameters.  Return the transform if X=None.

        Arguments
        ---------
        X : ANTsImage
            Image to transform

        y : ANTsImage (optional)
            Another image to transform

        Returns
        -------
        ANTsImage if y is None, else a tuple of ANTsImage types

        Examples
        --------
        >>> import ants
        >>> img = ants.image_read(ants.get_data('ch2'))
        >>> tx = ants.contrib.Zoom3D(zoom=(0.8,0.8,0.8))
        >>> img2 = tx.transform(img)
        '''
        # Generate random zoom parameters if zoom is a range
        if isinstance(self.zoom, (list, tuple)) and len(self.zoom) == 2:
            zoom_params = [np.random.uniform(self.zoom[0], self.zoom[1]) for _ in range(3)]
        elif isinstance(self.zoom, (list, tuple)) and len(self.zoom) == 3:
            zoom_params = self.zoom
        else:
            zoom_params = [self.zoom, self.zoom, self.zoom]
        
        # Create affine transform matrix
        transform_matrix = np.array([
            [1.0/zoom_params[0], 0, 0, 0],
            [0, 1.0/zoom_params[1], 0, 0],
            [0, 0, 1.0/zoom_params[2], 0],
            [0, 0, 0, 1]
        ])
        
        # Create ANTs transform
        if self.reference is not None:
            tx = ants.create_ants_transform(transform_type='AffineTransform', 
                                          precision='float', 
                                          dimension=3,
                                          matrix=transform_matrix[:3,:3],
                                          offset=transform_matrix[:3,3],
                                          reference=self.reference)
        else:
            tx = ants.create_ants_transform(transform_type='AffineTransform', 
                                          precision='float', 
                                          dimension=3,
                                          matrix=transform_matrix[:3,:3],
                                          offset=transform_matrix[:3,3])
        
        self.transform_ = tx
        
        if X is None:
            return tx
        
        if self.lazy:
            return tx
        
        # Apply transform to image(s)
        X_transformed = ants.apply_ants_transform_to_image(tx, X, reference=X)
        
        if y is None:
            return X_transformed
        else:
            y_transformed = ants.apply_ants_transform_to_image(tx, y, reference=y)
            return (X_transformed, y_transformed)