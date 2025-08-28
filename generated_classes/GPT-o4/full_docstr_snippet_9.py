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
        self.translation = tuple(translation)
        if len(self.translation) != 2:
            raise ValueError("Translate2D requires a 2-element translation.")
        self.reference = reference
        self.lazy = lazy

        # build affine transform parameters for 2D: [rot, tx, ty, sx, sy, skew]
        params = [0.0,
                  float(self.translation[0]),
                  float(self.translation[1]),
                  1.0, 1.0,
                  0.0]

        # fixed parameters: center of reference image
        if self.reference is not None:
            origin = np.array(self.reference.origin)
            spacing = np.array(self.reference.spacing)
            shape = np.array(self.reference.shape)
            center_index = (shape - 1) / 2.0
            phys_center = origin + spacing * center_index
            fixed_params = list(phys_center)
        else:
            fixed_params = None

        # create the ANTs affine transform
        self._transform = ants.create_ants_transform(
            transformtype='AffineTransform',
            dimension=2,
            parameters=params,
            fixed_parameters=fixed_params
        )

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
        '''
        if X is None or self.lazy:
            return self._transform

        if self.reference is None:
            raise ValueError("A reference image must be provided to apply the transform.")

        out_x = ants.apply_ants_transform_to_image(self._transform, X, self.reference)
        if y is None:
            return out_x
        out_y = ants.apply_ants_transform_to_image(self._transform, y, self.reference)
        return out_x, out_y