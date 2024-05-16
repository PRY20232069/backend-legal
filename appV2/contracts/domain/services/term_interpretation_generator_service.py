from abc import abstractmethod
from typing import List

class TermInterpretationGeneratorService:
    
    @abstractmethod
    def generate(self, terms: List[str]) -> List[str]:
        raise NotImplementedError()