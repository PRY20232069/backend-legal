from typing import Sequence
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from repositories.configuration.database import SessionLocal
from repositories.contract_repository import ContractRepository
from repositories.profile_repository import ProfileRepository
from repositories.term_repository import TermRepository
from resources.requests.get_terms_request import GetTermsRequest
from resources.requests.save_term_resource import SaveTermResource
from resources.responses.term_resource import TermResource
from services.terms_service import TermService
from utils.jwt_utils import JwtUtils

terms_router = APIRouter(
    prefix='/api/v1',
    tags=['Terms'],
)

router = terms_router

termSession = SessionLocal()
termRepository = TermRepository(termSession)
contractRepository = ContractRepository(termSession)
profileRepository = ProfileRepository(termSession)
termService = TermService(termRepository, contractRepository, profileRepository)

bearer_scheme = HTTPBearer()

@router.post("/contracts/{contract_id}/terms")
def register_term(saveTermResource: SaveTermResource, contract_id: int, token: str = Depends(bearer_scheme)) -> TermResource:
    user_id = JwtUtils.getUserId(token=token)
    termResource = termService.registerTerm(saveTermResource=saveTermResource, contract_id=contract_id, user_id=user_id)
    return termResource

@router.put("/contracts/{contract_id}/terms/{term_id}")
def generate_term_interpretation(contract_id: int, term_id: int, token: str = Depends(bearer_scheme)):
    user_id = JwtUtils.getUserId(token=token)
    termResource = termService.generateTermInterpretation(contract_id=contract_id, term_id=term_id, user_id=user_id)
    return termResource

@router.get("/contracts/{contract_id}/terms")
def get_all_terms_by_contract_id(contract_id: int, token: str = Depends(bearer_scheme)) -> Sequence[TermResource]:
    user_id = JwtUtils.getUserId(token=token)
    termsResource = termService.getAllTermsByContractId(contract_id, user_id)
    return termsResource

# @router.post("/terms/text")
# def identify_all_terms_by_text(getTermsRequest: GetTermsRequest) -> Sequence[TermResource]:
#     termsResource = termService.identifyAllTermsByText(getTermsRequest.text)
#     return termsResource

@router.get("/terms/admin")
def get_all_terms_only_admin() -> Sequence[TermResource]:
    termsResource = termService.getAllTermsByAdmin()
    return termsResource