class Assertion(object):

    def __init__(self, func, plugin_composite):
        self.func = func
        self.plugin_composite = plugin_composite

    def run(self, test_data):
        # call before hook if present
        before = getattr(self.plugin_composite, 'before_assertion', None)
        if callable(before):
            before(self, test_data)

        try:
            result = self.func(test_data)
            success = True
        except Exception as e:
            result = e
            success = False

        # call after hook if present
        after = getattr(self.plugin_composite, 'after_assertion', None)
        if callable(after):
            after(self, test_data, result, success)

        if not success:
            # re-raise the exception from the assertion
            raise result

        return result