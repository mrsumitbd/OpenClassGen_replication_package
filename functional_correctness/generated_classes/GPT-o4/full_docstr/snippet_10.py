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
        self.rotation_deg = rotation
        self.rotation_rad = math.radians(rotation)
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
        '''
        # Determine reference image for transform creation
        ref = self.reference if self.reference is not None else X
        if ref is None:
            raise ValueError("No reference or input image provided to define the transform space.")

        # Create the 2D Euler transform with the requested rotation (radians)
        tx = ants.create_ants_transform(
            transform_type='Euler2DTransform',
            fixed_image=ref,
            rotation=[self.rotation_rad]
        )

        # If no image to apply to, return the transform object
        if X is None:
            return tx

        # If lazy, return transform without applying
        if self.lazy:
            return tx

        # Apply transform to X (and y if given)
        x_t = ants.apply_ants_transform_to_image(tx, X, ref)
        if y is not None:
            y_t = ants.apply_ants_transform_to_image(tx, y, ref)
            return x_t, y_t
        return x_t