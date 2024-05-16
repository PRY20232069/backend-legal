from abc import abstractmethod
from fastapi import UploadFile

class FirebaseStorageService:
    
    @abstractmethod
    def save(self, filename: str, file: UploadFile) -> str:
        raise NotImplementedError()