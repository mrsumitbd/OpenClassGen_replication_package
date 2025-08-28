class Rotate2D(object):
    '''
    Create an ANTs Affine Transform with a specified level
    of rotation.
    '''

    def __init__(self, rotation, reference=None, lazy=False):
        '''
        Initialize a Rotate2D object

        Arguments
        ---------
        rotation : scalar
            rotation value in degrees.
            Negative values can be used for rotation in the
            other direction

        reference : ANTsImage (optional but recommended)
            image providing the reference space for the transform.
            this will also set the transform fixed parameters.

        lazy : boolean (default = False)
            if True, calling the `transform` method only returns
            the randomly generated transform and does not actually
            transform the image
        '''
        self.rotation = rotation
        self.reference = reference
        self.lazy = lazy

    def transform(self, X=None, y=None):
        '''
        Transform an image using an Affine transform with the given
        rotation parameters.   Return the transform if X=None.

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
        >>> img = ants.image_read(ants.get_data('r16'))
        >>> tx = ants.contrib.Rotate2D(rotation=(10,-5,12))
        >>> img2 = tx.transform(img)
        '''
        # Convert rotation from degrees to radians
        rotation_rad = math.radians(self.rotation)
        
        # Create rotation matrix parameters
        cos_theta = math.cos(rotation_rad)
        sin_theta = math.sin(rotation_rad)
        
        # Create affine transform
        tx = ants.create_ants_transform(transform_type='AffineTransform', dimension=2)
        
        # Set rotation matrix parameters
        matrix = [cos_theta, -sin_theta, sin_theta, cos_theta]
        tx.set_parameters(matrix + [0.0, 0.0])
        
        # Set fixed parameters if reference image is provided
        if self.reference is not None:
            center = [self.reference.shape[0] / 2.0, self.reference.shape[1] / 2.0]
            tx.set_fixed_parameters(center)
        elif X is not None:
            center = [X.shape[0] / 2.0, X.shape[1] / 2.0]
            tx.set_fixed_parameters(center)
        
        if X is None or self.lazy:
            return tx
        
        # Apply transform to image(s)
        if y is None:
            reference_img = self.reference if self.reference is not None else X
            return ants.apply_ants_transform_to_image(tx, X, reference_img)
        else:
            reference_img = self.reference if self.reference is not None else X
            X_transformed = ants.apply_ants_transform_to_image(tx, X, reference_img)
            y_transformed = ants.apply_ants_transform_to_image(tx, y, reference_img)
            return (X_transformed, y_transformed)