class Translate2D(object):
    '''
    Create an ANTs Affine Transform with a specified translation.
    '''

    def __init__(self, translation, reference=None, lazy=False):
        '''
        Initialize a Translate2D object

        Arguments
        ---------
        translation : list or tuple
            translation values for each axis, in degrees.
            Negative values can be used for translation in the
            other direction

        reference : ANTsImage (optional but recommended)
            image providing the reference space for the transform.
            this will also set the transform fixed parameters.

        lazy : boolean (default = False)
            if True, calling the `transform` method only returns
            the randomly generated transform and does not actually
            transform the image
        '''
        import ants
        
        self.translation = translation
        self.reference = reference
        self.lazy = lazy
        
        # Create the affine transform
        self.tx = ants.new_ants_transform(precision='float', dimension=2, transform_type='AffineTransform')
        
        # Set translation parameters (identity matrix with translation)
        # For 2D affine: [m11, m12, m21, m22, tx, ty]
        params = [1.0, 0.0, 0.0, 1.0, float(translation[0]), float(translation[1])]
        self.tx.set_parameters(params)
        
        # Set fixed parameters if reference is provided
        if reference is not None:
            # Fixed parameters are the center of rotation (origin)
            center = [0.0, 0.0]
            self.tx.set_fixed_parameters(center)

    def transform(self, X=None, y=None):
        '''
        Transform an image using an Affine transform with the given
        translation parameters.  Return the transform if X=None.

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
        >>> tx = ants.contrib.Translate2D(translation=(10,0))
        >>> img2_x = tx.transform(img)
        >>> tx = ants.contrib.Translate2D(translation=(-10,0)) # other direction
        >>> img2_x = tx.transform(img)
        >>> tx = ants.contrib.Translate2D(translation=(0,10))
        >>> img2_z = tx.transform(img)
        >>> tx = ants.contrib.Translate2D(translation=(10,10))
        >>> img2 = tx.transform(img)
        '''
        import ants
        
        if X is None:
            return self.tx
            
        if self.lazy:
            return self.tx
            
        reference_image = self.reference if self.reference is not None else X
        
        X_transformed = ants.apply_ants_transform_to_image(self.tx, X, reference_image)
        
        if y is not None:
            y_transformed = ants.apply_ants_transform_to_image(self.tx, y, reference_image)
            return (X_transformed, y_transformed)
        
        return X_transformed