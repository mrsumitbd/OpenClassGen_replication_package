class _AssertShapeLineStringsCheck(object):

    def __init__(self, shape):
        self.shape = shape

    def __call__(self, line_strings_on_images, _random_state, _parents,
                 _hooks):
        for ls_on_image in line_strings_on_images:
            if ls_on_image.shape != self.shape:
                raise AssertionError(
                    "Expected line strings to have shape %s, "
                    "but got %s." % (self.shape, ls_on_image.shape)
                )
        return line_strings_on_images