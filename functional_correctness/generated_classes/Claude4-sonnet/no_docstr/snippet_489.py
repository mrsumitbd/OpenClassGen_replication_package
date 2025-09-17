class _AssertShapeLineStringsCheck(object):

    def __init__(self, shape):
        self.shape = shape

    def __call__(self, line_strings_on_images, _random_state, _parents,
                 _hooks):
        for line_strings_on_image in line_strings_on_images:
            assert line_strings_on_image.shape == self.shape, \
                "Expected shape %s, got %s" % (self.shape, line_strings_on_image.shape)
        return line_strings_on_images