from typing import List, Sequence
from fastapi import HTTPException
from models.term import Term
from repositories.contract_repository import ContractRepository
from repositories.profile_repository import ProfileRepository
from repositories.term_repository import TermRepository
from resources.requests.save_user_resource import SaveUserResource
from resources.responses.term_resource import TermResource
from settings import OPENAI_API_KEY, OPENAI_MODEL_ID, OPENAI_SYSTEM_CONTENT
import openai

class TermService:
    def __init__(self, termRepository: TermRepository, contractRepository: ContractRepository, profileRepository: ProfileRepository):
        self.termRepository = termRepository
        self.contractRepository = contractRepository
        self.profileRepository = profileRepository

        openai.api_key = OPENAI_API_KEY
        self.openAIClient = openai

    def registerTerm(self, saveTermResource: SaveUserResource, contract_id, user_id) -> TermResource | Exception:
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


#     def generate_term_explanation_command(self, prompt: str):
#         # term_id = command.term_id
        
#         response = self.openAIClient.chat.completions.create(
#         model=self.openAISettings.model_id,
#         messages=[
#             {"role": "system", "content": "Eres un experto legal que explica por qué una cláusula puede ser o no potencialmente perjudicial para el consumidor"},
#             {"role": "user", "content": "Si en las fechas de pago de las Cuotas, la Cuenta de Pagos no tiene dinero (fondos) suficiente, el Banco podrá cobrar las Cuotas, así como, cualquier otro concepto establecido en la Hoja Resumen y/o en el Cronograma, de cualquier otra cuenta que Usted tenga en el Banco, sea en moneda nacional o en moneda extranjera.###"}
#         ]
#         )
#         print(response.choices[0].message.content)

#         explanationGeneratedEvent = TermExplanationGeneratedEvent(term_id=term_id, explanation=response.choices[0].message.content)

#         message = f'''
# **********************************************
#     TERM EXPLANATION GENERATED!!
#     term_id: {term_id}
#     explanation: {response.choices[0].message.content}
# **********************************************
#         '''

#         print(message)

#         return response.choices[0].message.content
    
    # def get_all_terms_by_contract_id_query(self, query: GetAllTermsByContractIdQuery):
    #     contract_id: int = query.contract_id
    #     terms: List[Term] = terms_examples
    #     return terms