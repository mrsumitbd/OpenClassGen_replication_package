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
        self.transform_obj = self._create_transform()

    def _create_transform(self):
        '''
        Create the affine transform object with the specified rotation
        '''
        # Create affine transform
        transform = ants.create_ants_transform(transform_type='AffineTransform', precision='float', dimension=2)
        
        # Convert rotation from degrees to radians
        rotation_rad = np.radians(self.rotation)
        
        # Create rotation matrix
        cos_theta = np.cos(rotation_rad)
        sin_theta = np.sin(rotation_rad)
        
        rotation_matrix = np.array([
            [cos_theta, -sin_theta],
            [sin_theta, cos_theta]
        ])
        
        # Set the transform parameters
        transform.set_parameters(rotation_matrix.flatten())
        
        # Set fixed parameters if reference is provided
        if self.reference is not None:
            transform.set_fixed_parameters(self.reference.get_center_of_mass())
            
        return transform

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
        if X is None:
            return self.transform_obj
            
        if self.lazy:
            return self.transform_obj
            
        # Apply transform to X
        X_transformed = ants.apply_ants_transform_to_image(self.transform_obj, X, reference=self.reference)
        
        if y is None:
            return X_transformed
        else:
            # Apply transform to y as well
            y_transformed = ants.apply_ants_transform_to_image(self.transform_obj, y, reference=self.reference)
            return (X_transformed, y_transformed)