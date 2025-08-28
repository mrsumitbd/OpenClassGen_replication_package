class ErrorSanitizer(object):

    def __init__(self, password):
        self._password = '' if password is None else str(password)

    @staticmethod
    def clean(error):
        # Convert exceptions or any object to a plain string
        if isinstance(error, BaseException):
            try:
                # If the exception has args, join them
                return ' '.join(str(arg) for arg in error.args)
            except Exception:
                return str(error)
        return str(error)

    def scrub(self, error):
        """
        Return a sanitized string form of the error,
        masking any occurrence of the stored password.
        """
        msg = self.clean(error)
        if self._password:
            mask = '*' * len(self._password)
            # escape the password for safe literal replacement
            import re
            pattern = re.escape(self._password)
            msg = re.sub(pattern, mask, msg)
        return msg