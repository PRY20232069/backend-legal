from fastapi import HTTPException
from fastapi import UploadFile
from firebase_admin import storage

from appV2.contracts.domain.services.firebase_storage_service import FirebaseStorageService

class FirebaseStorageServiceImpl(FirebaseStorageService):
    
    def save(self, filename: str, file: UploadFile) -> str:
        bucket = storage.bucket()
        blob = bucket.blob(filename)

        file.file.seek(0)
        file_data = file.file.read()
        
        try:
            blob.upload_from_string(
                data=file_data,
                content_type='application/pdf'
            )
            blob.make_public()
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail="Error uploading file. Please try again.")

        return blob.public_url