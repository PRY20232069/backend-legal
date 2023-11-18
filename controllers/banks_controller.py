from typing import Sequence
from fastapi import APIRouter
from fastapi.security import HTTPBearer
from repositories.bank_repository import BankRepository

from repositories.configuration.database import SessionLocal
from repositories.contract_repository import ContractRepository
from resources.requests.save_bank_resource import SaveBankResource
from resources.responses.bank_resource import BankResource
from services.bank_service import BankService

banks_router = APIRouter(
    prefix='/api/v1/banks',
    tags=['Banks'],
)

router = banks_router

bankSession = SessionLocal()
bankRepository = BankRepository(bankSession)
contractRepository = ContractRepository(bankSession)
bankService = BankService(bankRepository, contractRepository)

bearer_scheme = HTTPBearer()

@router.post("/")
def register_bank(saveBankResource: SaveBankResource) -> BankResource:
    bank_resource = bankService.createBank(saveBankResource=saveBankResource)
    return bank_resource

@router.get("/")
def get_all_banks() -> Sequence[BankResource]:
    bankResources = bankService.getAllBanks()
    return bankResources