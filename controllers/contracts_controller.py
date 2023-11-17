from typing import Sequence
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.security import HTTPBearer
from repositories.bank_repository import BankRepository

from repositories.configuration.database import SessionLocal
from repositories.contract_repository import ContractRepository
from repositories.profile_repository import ProfileRepository
from repositories.term_repository import TermRepository
from resources.requests.save_contract_resource import SaveContractResource
from resources.responses.contract_resource import ContractResource
from resources.responses.term_resource import TermResource
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
termRepository = TermRepository(contractSession)
contractService = ContractService(contractRepository, profileRepository, bankRepository, termRepository)

bearer_scheme = HTTPBearer()

@router.post("/")
async def create_contract(saveContractResource: SaveContractResource, token: str = Depends(bearer_scheme)) -> ContractResource:
    user_id = JwtUtils.getUserId(token=token)
    contractResource = contractService.createContract(saveContractResource=saveContractResource, user_id=user_id)
    return contractResource

@router.put("/{contract_id}")
async def upload_pdf(contract_id: int, file: UploadFile = File(...), token: str = Depends(bearer_scheme)) -> ContractResource:
    user_id = JwtUtils.getUserId(token=token)
    contractResource = await contractService.uploadPDF(file=file, contract_id=contract_id, user_id=user_id)
    return contractResource

@router.put("/{contract_id}/termsinterpretations")
def generate_terms_interprations_by_contract_id(contract_id: int, token: str = Depends(bearer_scheme)) -> Sequence[TermResource]:
    user_id = JwtUtils.getUserId(token=token)
    termResources = contractService.generateTermsInterprationsByContractId(contract_id=contract_id, user_id=user_id)
    return termResources

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