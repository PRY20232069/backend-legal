from typing import Sequence
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from repositories.bank_repository import BankRepository

from repositories.configuration.database import SessionLocal
from repositories.contract_repository import ContractRepository
from repositories.profile_repository import ProfileRepository
from resources.requests.save_contract_resource import SaveContractResource
from resources.responses.contract_resource import ContractResource
from services.contract_service import ContractService
from utils.jwt_utils import JwtUtils

contracts_router = APIRouter(
    prefix='/api/v1/contracts',
    tags=['Contracts'],
)

router = contracts_router

contractSession = SessionLocal()
contractRepository = ContractRepository(contractSession)
profileRepository = ProfileRepository(contractSession)
bankRepository = BankRepository(contractSession)
contractService = ContractService(contractRepository, profileRepository, bankRepository)

bearer_scheme = HTTPBearer()

@router.post("/")
def upload_contract(saveContractResource: SaveContractResource, token: str = Depends(bearer_scheme)) -> ContractResource:
    user_id = JwtUtils.getUserId(token=token)
    contractResource = contractService.uploadContract(saveContractResource=saveContractResource, user_id=user_id)
    return contractResource

@router.get("/")
def get_all_contracts(token: str = Depends(bearer_scheme)) -> Sequence[ContractResource]:
    user_id = JwtUtils.getUserId(token=token)
    contractsResource = contractService.getAllContracts(user_id=user_id)
    return contractsResource

@router.get("/search/{name}")
def get_all_contracts_by_name(name: str, token: str = Depends(bearer_scheme)) -> Sequence[ContractResource]:
    user_id = JwtUtils.getUserId(token=token)
    contractsResource = contractService.getAllContractsByName(name=name, user_id=user_id)
    return contractsResource

@router.get("/admin")
def get_all_contracts_only_admin() -> Sequence[ContractResource]:
    contractsResource = contractService.getAllContractsByAdmin()
    return contractsResource

@router.get("/{contract_id}")
def get_contract_by_id(contract_id: int, token: str = Depends(bearer_scheme)) -> ContractResource:
    user_id = JwtUtils.getUserId(token=token)
    contractResource = contractService.getContractByContractId(contract_id=contract_id, user_id=user_id)
    return contractResource