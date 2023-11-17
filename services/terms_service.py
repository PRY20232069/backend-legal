from typing import List, Sequence
from fastapi import HTTPException
from models.term import Term
from repositories.contract_repository import ContractRepository
from repositories.profile_repository import ProfileRepository
from repositories.term_repository import TermRepository
from resources.requests.save_term_resource import SaveTermResource
from resources.responses.term_resource import TermResource
from settings import OPENAI_API_KEY, OPENAI_MODEL_ID, OPENAI_SYSTEM_CONTENT, OPENAI_SYSTEM_CONTENT_TERMS_INDETIFYIER
import openai

class TermService:
    def __init__(self, termRepository: TermRepository, contractRepository: ContractRepository, profileRepository: ProfileRepository):
        self.termRepository = termRepository
        self.contractRepository = contractRepository
        self.profileRepository = profileRepository

        openai.api_key = OPENAI_API_KEY
        self.openAIClient = openai
        self.openAIClient.api_timeout = 360 # 6 minutos

    def registerTerm(self, saveTermResource: SaveTermResource, contract_id, user_id) -> TermResource | Exception:
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
        
        term = self.termRepository.create(saveTermResource.to_model(contract_id=contract_id))
        return term.to_resource()
    
    def generateTermInterpretation(self, contract_id, term_id, user_id) -> TermResource | Exception:
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
        
        existingTerm = self.termRepository.find_by_term_id_and_contract_id(term_id=term_id, contract_id=contract_id)
        if not existingTerm:
            raise HTTPException(
                status_code=404,
                detail="Term not found"
            )
        
        existingTerm.interpretation = self.__generate_term_interpretation__(existingTerm.description)
        term = self.termRepository.update(existingTerm)
        
        return term.to_resource()
    
    def getAllTermsByContractId(self, contract_id, user_id) -> Sequence[TermResource] | Exception:
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
        return [term.to_resource() for term in terms]
    
    def identifyAllTermsByText(self, text: str) -> Sequence[TermResource] | Exception:
        terms = self.__identify_terms_in_text__(text) # Esta funcion retorna un texto con varios parrafos separados por ???. Ahora debemos obtener por cada parrafo un TermResource
        terms = terms.split('???')
        termResources = [TermResource(description=term, index=index) for index, term in enumerate(terms)]
        return termResources

    def getAllTermsByAdmin(self) -> Sequence[TermResource]:
        terms = self.termRepository.find_all()
        return [term.to_resource() for term in terms]

#############

    def __generate_term_interpretation__(self, term_description: str) -> str:
        response = self.openAIClient.chat.completions.create(
            model=OPENAI_MODEL_ID,
            messages=[
                {"role": "system", "content": OPENAI_SYSTEM_CONTENT},
                {"role": "user", "content": f"{term_description}###"}
            ]
        )
        return response.choices[0].message.content
    
    
    def __identify_terms_in_text__(self, text: str) -> str:
        response = self.openAIClient.chat.completions.create(
            model='gpt-4-1106-preview',
            messages=[
                {"role": "system", "content": OPENAI_SYSTEM_CONTENT_TERMS_INDETIFYIER},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content