from abc import abstractmethod

class PasswordHasherService:
    
    @abstractmethod
    def hash(self, secret: str) -> str:
        raise NotImplementedError()
        
    @abstractmethod
    def verify(self, secret: str, hash: str) -> bool:
        raise NotImplementedError()