import os
from fastapi import UploadFile

from appV2.contracts.domain.services.pdf_validator_service import PdfValidatorService

class PdfValidatorServiceImpl(PdfValidatorService):
    
    async def validate(self, file: UploadFile) -> bool:
        _, file_extension = os.path.splitext(file.filename)
        if file_extension.lower() != '.pdf':
            return False

        # Check file MIME type
        content = await file.read()
        if content[:4] != b'%PDF':
            return False

        return True