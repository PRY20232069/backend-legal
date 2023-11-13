from typing import Sequence
from fastapi import HTTPException
from repositories.bank_repository import BankRepository
from repositories.contract_repository import ContractRepository
from repositories.profile_repository import ProfileRepository
from resources.requests.save_contract_resource import SaveContractResource
from resources.responses.contract_resource import ContractResource


class ContractService:
    def __init__(self, contractRepository: ContractRepository, profileRepository: ProfileRepository, bankRepository: BankRepository):
        self.contractRepository = contractRepository
        self.profileRepository = profileRepository
        self.bankRepository = bankRepository

    def uploadContract(self, saveContractResource: SaveContractResource, user_id) -> ContractResource | Exception:
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
    
