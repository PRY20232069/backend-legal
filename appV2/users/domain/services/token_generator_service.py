from abc import abstractmethod

class TokenGeneratorService:
    
    @abstractmethod
    def generate(self, id: int) -> str:
        raise NotImplementedError()