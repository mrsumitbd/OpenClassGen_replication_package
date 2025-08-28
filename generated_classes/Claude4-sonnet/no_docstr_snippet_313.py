class AuthenticatesTokens:
    def __init__(self, secret_key: str = "default_secret_key", algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def generate_jwt(self, payload: Optional[Dict[str, Any]] = None, expires_in: int = 3600) -> str:
        if payload is None:
            payload = {}
        
        # Add expiration time
        payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
        payload['iat'] = datetime.datetime.utcnow()
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def attempt_by_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            decoded_payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return decoded_payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        except Exception:
            return None