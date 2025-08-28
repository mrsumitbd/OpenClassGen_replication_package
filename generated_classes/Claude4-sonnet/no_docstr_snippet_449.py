class Assertion(object):

    def __init__(self, func, plugin_composite):
        self.func = func
        self.plugin_composite = plugin_composite

    def run(self, test_data):
        return self.func(test_data, self.plugin_composite)