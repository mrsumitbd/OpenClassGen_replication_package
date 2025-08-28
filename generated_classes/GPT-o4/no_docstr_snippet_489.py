class _AssertShapeLineStringsCheck(object):
    def __init__(self, shape):
        # store expected shape
        self.shape = tuple(shape)

    def __call__(self, line_strings_on_images, _random_state, _parents, _hooks):
        # verify that each LineStringsOnImage has the expected shape
        for ls in line_strings_on_images:
            actual = getattr(ls, "shape", None)
            if actual != self.shape:
                raise AssertionError(
                    "Expected LineStringsOnImage.shape to be {0}, got {1}.".format(
                        self.shape, actual
                    )
                )
        return line_strings_on_images