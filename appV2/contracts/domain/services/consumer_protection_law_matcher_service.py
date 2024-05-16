from abc import abstractmethod
from typing import List

class ConsumerProtectionLawMatcherService:
    
    @abstractmethod
    def match(self, terms: List[str]) -> List[str]:
        raise NotImplementedError()