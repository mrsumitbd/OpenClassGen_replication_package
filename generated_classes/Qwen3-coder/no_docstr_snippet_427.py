class ErrorSanitizer(object):

    def __init__(self, password):
        self.password = password

    @staticmethod
    def clean(error):
        if isinstance(error, Exception):
            return str(error)
        return error

    def scrub(self, error):
        if isinstance(error, Exception):
            error_str = str(error)
            if self.password in error_str:
                return error_str.replace(self.password, '*' * len(self.password))
            return error_str
        elif isinstance(error, str):
            if self.password in error:
                return error.replace(self.password, '*' * len(self.password))
            return error
        return error