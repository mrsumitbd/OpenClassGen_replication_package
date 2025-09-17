class AuthenticatesTokens:
    def __init__(self, payload, secret_key, algorithm='HS256', expiration=3600):
        self.payload = payload
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expiration = expiration

    def generate_jwt(self):
        data = self.payload.copy()
        data['exp'] = datetime.utcnow() + timedelta(seconds=self.expiration)
        token = jwt.encode(data, self.secret_key, algorithm=self.algorithm)
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        return token

    def attempt_by_token(self, token):
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None