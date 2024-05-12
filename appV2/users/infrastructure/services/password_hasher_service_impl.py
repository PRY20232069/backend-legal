from passlib.context import CryptContext

from appV2.users.domain.services.password_hasher_service import PasswordHasherService

class PasswordHasherServiceImpl(PasswordHasherService):
    def __init__(self):
        self.hasher = CryptContext(schemes=["bcrypt"])
    
    def hash(self, secret: str) -> str:
        return self.hasher.hash(secret)
        
    def verify(self, secret: str, hash: str) -> bool:
        return self.hasher.verify(secret, hash)