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
        zoom_range : list or tuple
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
        if isinstance(self.zoom, (list, tuple)) and len(self.zoom) == 3:
            zoom_params = self.zoom
        else:
            zoom_params = [self.zoom] * 3
        
        matrix = np.eye(4)
        matrix[0, 0] = zoom_params[0]
        matrix[1, 1] = zoom_params[1]
        matrix[2, 2] = zoom_params[2]
        
        tx = ants.create_ants_transform(transform_type='AffineTransform', 
                                       dimension=3, 
                                       matrix=matrix)
        
        if self.reference is not None:
            tx.set_fixed_parameters(self.reference.origin + self.reference.spacing + self.reference.direction.flatten().tolist())
        
        if X is None or self.lazy:
            return tx
        
        X_transformed = ants.apply_ants_transform_to_image(tx, X, X if self.reference is None else self.reference)
        
        if y is None:
            return X_transformed
        else:
            y_transformed = ants.apply_ants_transform_to_image(tx, y, y if self.reference is None else self.reference)
            return X_transformed, y_transformed