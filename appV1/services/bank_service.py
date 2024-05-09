from typing import Sequence
from fastapi import HTTPException
from appV1.repositories.bank_repository import BankRepository
from appV1.repositories.contract_repository import ContractRepository
from appV1.resources.requests.save_bank_resource import SaveBankResource
from appV1.resources.responses.bank_resource import BankResource


class BankService:
    def __init__(self, bankRepository: BankRepository, contractRepository: ContractRepository):
        self.bankRepository = bankRepository
        self.contractRepository = contractRepository

    def createBank(self, saveBankResource: SaveBankResource) -> BankResource | Exception:
        existingBank = self.bankRepository.find_by_name(name=saveBankResource.name)
        if existingBank:
            raise HTTPException(
                status_code=409,
                detail="Bank already exists"
            )
        
        bank = self.bankRepository.create(saveBankResource.to_model())
        return bank.to_resource()
    
    def getAllBanks(self) -> Sequence[BankResource]:
        banks = self.bankRepository.find_all()

        bankResources = []
        for bank in banks:
            contracts_count = self.contractRepository.get_count_by_bank_id(bank.id)
            bankResources.append(bank.to_resource(contracts_count=contracts_count))

        return bankResources