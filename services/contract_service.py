import io
import os
import re
import openai
from typing import Sequence
from PyPDF2 import PdfReader
from fastapi import HTTPException
from firebase_admin import storage
from repositories.bank_repository import BankRepository
from repositories.term_repository import TermRepository
from repositories.profile_repository import ProfileRepository
from repositories.contract_repository import ContractRepository
from resources.requests.save_term_resource import SaveTermResource
from resources.responses.contract_resource import ContractResource
from resources.requests.save_contract_resource import SaveContractResource
from resources.responses.term_resource import TermResource
from settings import OPENAI_API_KEY, OPENAI_MODEL_ID, OPENAI_SYSTEM_CONTENT
from utils.consumer_protection_law_matcher import ConsumerProtectionLawMatcher


class ContractService:
    def __init__(self, contractRepository: ContractRepository, profileRepository: ProfileRepository, bankRepository: BankRepository, termRepository: TermRepository):
        self.contractRepository = contractRepository
        self.profileRepository = profileRepository
        self.bankRepository = bankRepository
        self.termRepository = termRepository

        openai.api_key = OPENAI_API_KEY
        self.openAIClient = openai
        self.openAIClient.api_timeout = 360 # 6 minutos

        self.consumerProtectionLawMatcher = ConsumerProtectionLawMatcher()

    def createContract(self, saveContractResource: SaveContractResource, user_id) -> ContractResource | Exception:
        existingBank = self.bankRepository.find_by_id(saveContractResource.bank_id)
        if not existingBank:
            raise HTTPException(
                status_code=404,
                detail="Bank not found"
            )

        existingProfile = self.profileRepository.find_by_user_id(user_id=user_id)
        if not existingProfile:
            raise HTTPException(
                status_code=404,
                detail="Profile not found"
            )
        
        finalName = saveContractResource.name
        
        existingContract = self.contractRepository.find_by_name_and_profile_id(name=saveContractResource.name, profile_id=existingProfile.id)
        if existingContract:
            i = 1
            can_search = True
            while can_search:
                finalName = saveContractResource.name + ' (' + str(i) + ')'
                i += 1
                sameNameContract = self.contractRepository.find_by_name_and_profile_id(name=finalName, profile_id=existingProfile.id)
                if not sameNameContract:
                    can_search = False

        saveContractResource.name = finalName
        contract = self.contractRepository.create(saveContractResource.to_model(profile_id=existingProfile.id))
        return contract.to_resource()
    
    def updateContract(self, contract_id: int, saveContractResource: SaveContractResource, user_id) -> ContractResource | Exception:
        existingBank = self.bankRepository.find_by_id(saveContractResource.bank_id)
        if not existingBank:
            raise HTTPException(
                status_code=404,
                detail="Bank not found"
            )

        existingProfile = self.profileRepository.find_by_user_id(user_id=user_id)
        if not existingProfile:
            raise HTTPException(
                status_code=404,
                detail="Profile not found"
            )
        
        existingContract = self.contractRepository.find_by_contract_id_and_profile_id(contract_id=contract_id, profile_id=existingProfile.id)
        if not existingContract:
            raise HTTPException(
                status_code=404,
                detail="Contract not found"
            )
        
        existingContract.name = saveContractResource.name
        existingContract.favorite = saveContractResource.favorite

        contract = self.contractRepository.update(existingContract)
        return contract.to_resource()
    
    async def uploadPDF(self, file, contract_id, user_id) -> ContractResource | Exception:
        existingProfile = self.profileRepository.find_by_user_id(user_id=user_id)
        if not existingProfile:
            raise HTTPException(
                status_code=404,
                detail="Profile not found"
            )
        
        isValidFile = await self.__validatePDF__(file=file)
        if not isValidFile:
            raise HTTPException(
                status_code=400,
                detail="Invalid file"
            )
        
        existingContract = self.contractRepository.find_by_contract_id_and_profile_id(contract_id=contract_id, profile_id=existingProfile.id)
        if not existingContract:
            raise HTTPException(
                status_code=404,
                detail="Contract not found"
            )
        
        file_name = f"{existingProfile.id}__{existingContract.name.replace('.pdf', '')}.pdf"  # 6__ContratoDePrestamo.pdf
        file_url = self.__saveFile__(file=file, file_name=file_name)
        existingContract.file_url = file_url

        contract = self.contractRepository.update(existingContract)
        
        result = self.__separateParagraphsFromPdf__(file=file, contract_id=contract.id)

        if not result:
            raise HTTPException(
                status_code=400,
                detail="Error uploading file. Please try again."
            )
        
        return contract.to_resource()
    
    def generateTermsInterprationsByContractId(self, contract_id, user_id) -> Sequence[TermResource] | Exception:
        existingProfile = self.profileRepository.find_by_user_id(user_id=user_id)
        if not existingProfile:
            raise HTTPException(
                status_code=404,
                detail="Profile not found"
            )
        
        existingContract = self.contractRepository.find_by_contract_id_and_profile_id(contract_id=contract_id, profile_id=existingProfile.id)
        if not existingContract:
            raise HTTPException(
                status_code=404,
                detail="Contract not found"
            )
        
        terms = self.termRepository.find_all_by_contract_id(contract_id=contract_id)

        for term in terms:
            term.interpretation = self.__generate_term_interpretation__(term.description)
            self.termRepository.update(term)

        return [term.to_resource() for term in terms]
    
    def matchTermsWithConsumerProtectionLawsByContractId(self, contract_id, user_id) -> Sequence[TermResource] | Exception:
        existingProfile = self.profileRepository.find_by_user_id(user_id=user_id)
        if not existingProfile:
            raise HTTPException(
                status_code=404,
                detail="Profile not found"
            )
        
        existingContract = self.contractRepository.find_by_contract_id_and_profile_id(contract_id=contract_id, profile_id=existingProfile.id)
        if not existingContract:
            raise HTTPException(
                status_code=404,
                detail="Contract not found"
            )
        
        terms = self.termRepository.find_all_by_contract_id(contract_id=contract_id)

        for term in terms:
            term.consumer_protection_law = self.__match_term_with_consumer_protection_law__(term.description)
            self.termRepository.update(term)

        return [term.to_resource() for term in terms]
    
    def getAllContracts(self, user_id) -> Sequence[ContractResource]:
        existingProfile = self.profileRepository.find_by_user_id(user_id=user_id)
        if not existingProfile:
            raise HTTPException(
                status_code=404,
                detail="Profile not found"
            )
        
        contracts = self.contractRepository.find_all_by_profile_id(profile_id=existingProfile.id)
        return [contract.to_resource() for contract in contracts]
    
    def getAllContractsByName(self, name: str, user_id) -> Sequence[ContractResource]:
        existingProfile = self.profileRepository.find_by_user_id(user_id=user_id)
        if not existingProfile:
            raise HTTPException(
                status_code=404,
                detail="Profile not found"
            )
        
        contracts = self.contractRepository.find_all_by_name_and_profile_id(name=name, profile_id=existingProfile.id)
        return [contract.to_resource() for contract in contracts]
    
    def getAllContractsByAdmin(self) -> Sequence[ContractResource]:
        contracts = self.contractRepository.find_all()
        return [contract.to_resource() for contract in contracts]
    
    def getContractByContractId(self, contract_id: int, user_id) -> ContractResource | Exception:
        existingProfile = self.profileRepository.find_by_user_id(user_id=user_id)
        if not existingProfile:
            raise HTTPException(
                status_code=404,
                detail="Profile not found"
            )
        
        existingContract = self.contractRepository.find_by_contract_id_and_profile_id(contract_id=contract_id, profile_id=existingProfile.id)
        if not existingContract:
            raise HTTPException(
                status_code=404,
                detail="Contract not found"
            )
        
        return existingContract.to_resource()
    
#########
    

    async def __validatePDF__(self, file) -> bool:
        # Check file extension
        _, file_extension = os.path.splitext(file.filename)
        if file_extension.lower() != '.pdf':
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF file.")

        # Check file MIME type
        content = await file.read()
        if content[:4] != b'%PDF':
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF file.")
        
        return True
    
    def __saveFile__(self, file, file_name) -> str:
        # Get a reference to the storage service
        bucket = storage.bucket()

        # Create a new blob with the file name
        blob = bucket.blob(file_name)

        # Move the "cursor" back to the start of the file
        file.file.seek(0)

        file_data = file.file.read()
        # print('PRINTING FILE DATA')
        # print(file_data)
        # print('FILE DATA PRINTED')

        # Upload the file content
        try:
            blob.upload_from_string(
                data=file_data,
                content_type='application/pdf'
            )

            # Make the blob publicly readable
            blob.make_public()
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail="Error uploading file. Please try again.")

        # Return the public url of the uploaded file
        return blob.public_url
    
    def __separateParagraphsFromPdf__(self, file, contract_id) -> bool:
        # Move the "cursor" back to the start of the file
        file.file.seek(0)

        # Read the file content
        file_data = file.file.read()

        # Create a PDF file reader
        pdf_reader = PdfReader(io.BytesIO(file_data))

        try: 
            # Read the content of the PDF
            for page_number, page in enumerate(pdf_reader.pages):
                content = page.extract_text()

                # Split the content by paragraphs
                paragraphs = re.split(r'\.\s*\n', content)

                for index, paragraph in enumerate(paragraphs):
                    saveTermResource = SaveTermResource(description=paragraph, index=index, num_page=page_number)
                    self.termRepository.create(saveTermResource.to_model(contract_id=contract_id))
        except Exception as e:
            print(e)
            return False
            
        return True

    def __generate_term_interpretation__(self, term_description: str) -> str:
        response = self.openAIClient.chat.completions.create(
            model=OPENAI_MODEL_ID,
            messages=[
                {"role": "system", "content": OPENAI_SYSTEM_CONTENT},
                {"role": "user", "content": f"{term_description}###"}
            ]
        )
        return response.choices[0].message.content
    
    def __match_term_with_consumer_protection_law__(self, term_description: str) -> str:
        consumer_protection_law = self.consumerProtectionLawMatcher.getConsumerProtectionLaw(term_description)
        return consumer_protection_law