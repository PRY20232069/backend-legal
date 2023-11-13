import jwt
from settings import ALGORITHM, SECRET_KEY

class JwtUtils:
    
    @staticmethod
    def getUserId(token: str):
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("id")