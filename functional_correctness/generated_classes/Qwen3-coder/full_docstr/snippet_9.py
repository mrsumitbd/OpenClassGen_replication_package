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
        self.translation = translation
        self.reference = reference
        self.lazy = lazy
        
        # Create the affine transform
        self.transform_obj = ants.create_ants_transform(
            transform_type='AffineTransform',
            precision='float',
            dimension=2
        )
        
        # Set the translation parameters
        # For affine transform, parameters are [cos, -sin, sin, cos, tx, ty]
        # For pure translation: [1, 0, 0, 1, tx, ty]
        tx, ty = translation
        parameters = [1, 0, 0, 1, tx, ty]
        self.transform_obj.set_parameters(parameters)
        
        # Set fixed parameters if reference is provided
        if reference is not None:
            self.transform_obj.set_fixed_parameters(reference.get_origin())

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
        if X is None:
            return self.transform_obj
            
        if self.lazy:
            return self.transform_obj
            
        # Apply transform to X
        X_transformed = ants.apply_ants_transform_to_image(
            self.transform_obj, X, reference=X
        )
        
        if y is None:
            return X_transformed
        else:
            # Apply transform to y
            y_transformed = ants.apply_ants_transform_to_image(
                self.transform_obj, y, reference=y
            )
            return (X_transformed, y_transformed)