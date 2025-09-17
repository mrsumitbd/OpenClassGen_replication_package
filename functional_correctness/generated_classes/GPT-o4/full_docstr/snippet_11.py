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
        zoom : scalar, 2-tuple, 3-tuple, or tuple of 3 2-tuples
            If scalar or 3-tuple of scalars, use fixed zoom factors.
            If 2-tuple of scalars, draw each of 3 axes from that range.
            If 3-tuple of 2-tuples, draw each axis from its own range.
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
        self._last_zoom = None

    def _draw_zoom(self):
        z = self.zoom
        if np.isscalar(z):
            return [float(z)] * 3
        z = tuple(z)
        if len(z) == 2 and all(np.isscalar(v) for v in z):
            lo, hi = z
            return [float(np.random.uniform(lo, hi)) for _ in range(3)]
        if len(z) == 3:
            out = []
            for v in z:
                if np.isscalar(v):
                    out.append(float(v))
                elif len(v) == 2 and all(np.isscalar(x) for x in v):
                    out.append(float(np.random.uniform(v[0], v[1])))
                else:
                    raise ValueError("Each element must be scalar or 2-tuple of scalars.")
            return out
        raise ValueError("Invalid zoom specification.")

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
        '''
        # draw zoom factors
        zoom_factors = self._draw_zoom()
        self._last_zoom = tuple(zoom_factors)

        # pick reference for center
        ref = self.reference
        if ref is None:
            if X is None:
                raise ValueError("Reference image or X must be provided to build transform.")
            ref = X

        dim = ref.dimension
        if dim != 3:
            raise ValueError("Zoom3D only supports 3D images.")

        # compute center in physical space
        origin = np.array(ref.origin)
        spacing = np.array(ref.spacing)
        shape = np.array(ref.shape)
        direction = np.array(ref.direction).reshape((dim, dim))
        idx_center = (shape - 1) / 2.0
        phys_center = origin + direction.dot(spacing * idx_center)

        # build affine matrix and translation
        S = np.diag(zoom_factors)
        M = S
        c = phys_center
        t = (np.eye(dim) - M).dot(c)

        # parameters: row-major matrix then translation
        params = list(M.flatten()) + list(t)
        fparams = list(phys_center)

        tx = ants.create_ants_transform('AffineTransform', dim, parameters=params, fixedParameters=fparams)

        # if requested to only return transform
        if X is None or self.lazy:
            return tx

        # apply to X (and y if provided)
        outX = ants.apply_ants_transform_to_image(tx, X, ref)
        if y is None:
            return outX
        outY = ants.apply_ants_transform_to_image(tx, y, ref)
        return outX, outY