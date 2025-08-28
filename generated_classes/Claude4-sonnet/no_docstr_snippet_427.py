class ErrorSanitizer(object):

    def __init__(self, password):
        self.password = password

    @staticmethod
    def clean(error):
        import re
        # Remove common sensitive patterns
        patterns = [
            r'password[=:\s]+[^\s\n]+',
            r'token[=:\s]+[^\s\n]+',
            r'key[=:\s]+[^\s\n]+',
            r'secret[=:\s]+[^\s\n]+',
            r'api_key[=:\s]+[^\s\n]+',
            r'auth[=:\s]+[^\s\n]+',
            r'credential[=:\s]+[^\s\n]+',
        ]
        
        cleaned_error = str(error)
        for pattern in patterns:
            cleaned_error = re.sub(pattern, lambda m: m.group().split('=')[0] + '=***' if '=' in m.group() else m.group().split(':')[0] + ':***' if ':' in m.group() else m.group().split()[0] + ' ***', cleaned_error, flags=re.IGNORECASE)
        
        return cleaned_error

    def scrub(self, error):
        error_str = str(error)
        if self.password and self.password in error_str:
            error_str = error_str.replace(self.password, '***')
        return self.clean(error_str)