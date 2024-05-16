import io
import re
from abc import abstractmethod
from fastapi import UploadFile
from PyPDF2 import PdfReader
from typing import List

from appV2.contracts.domain.services.document_processor_service import DocumentProcessorService

class DocumentProcessorServiceImpl(DocumentProcessorService):
    
    def split_paragraphs(self, file: UploadFile) -> List[str]:
        file.file.seek(0)
        file_data = file.file.read()

        pdf_reader = PdfReader(io.BytesIO(file_data))
        result_paragraphs: List[str] = []

        for page_number, page in enumerate(pdf_reader.pages):
            content = page.extract_text()
            paragraphs = re.split(r'\.\s*\n', content)
            result_paragraphs.extend([paragraph.strip() for paragraph in paragraphs if paragraph.strip()])
            
        return result_paragraphs