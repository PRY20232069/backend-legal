from abc import abstractmethod
from fastapi import UploadFile
from typing import List

class DocumentProcessorService:
    
    @abstractmethod
    def split_paragraphs(self, file: UploadFile) -> List[str]:
        raise NotImplementedError()