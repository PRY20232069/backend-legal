from abc import abstractmethod
from fastapi import UploadFile

class PdfValidatorService:
    
    @abstractmethod
    def validate(self, file: UploadFile) -> bool:
        raise NotImplementedError()