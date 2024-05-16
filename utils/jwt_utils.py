import jwt
from datetime import datetime
from fastapi.security import HTTPAuthorizationCredentials

from settings import ALGORITHM, SECRET_KEY

class JwtUtils:

    @staticmethod
    def is_valid(token: HTTPAuthorizationCredentials):
        token = token.credentials
        return True
    
    @staticmethod
    def get_user_id(token: HTTPAuthorizationCredentials):
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("id")
        
####################################


    @staticmethod
    def is_invalid(token: str):
        parts = token.split(" ")
        if len(parts) != 2 or parts[0] != "Bearer":
            return True
        return False
    
    @staticmethod
    def get_user_id2(token: str):
        toke_parts = token.split(" ")
        payload = jwt.decode(toke_parts[1], SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("id")

    @staticmethod
    def is_expired(token: str) -> bool:
        try:
            toke_parts = token.split(" ")
            payload = jwt.decode(toke_parts[1], SECRET_KEY, algorithms=[ALGORITHM])
            expiration_timestamp = payload.get("exp")
            current_timestamp = datetime.utcnow().timestamp()
            return expiration_timestamp < current_timestamp
        except jwt.ExpiredSignatureError as e:
            print(e)
            return True
        except Exception as e:
            print(e)
            return False
