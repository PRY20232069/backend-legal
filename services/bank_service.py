from typing import Sequence
from fastapi import HTTPException
from repositories.bank_repository import BankRepository
from resources.requests.save_bank_resource import SaveBankResource
from resources.responses.bank_resource import BankResource


class BankService:
    def __init__(self, bankRepository: BankRepository):
        self.bankRepository = bankRepository

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
        return [bank.to_resource() for bank in banks]