from typing import List
from fastapi import Depends, HTTPException, status, Response, Request, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError, TokenExpiredError, TokenInvalidError
from appV2.contracts.application.exceptions.contract_exceptions import ContractNotFoundError
from appV2.contracts.interfaces.REST.controllers.contracts_controller import router
from appV2.contracts.interfaces.REST.resources.term_resource import TermResource
from appV2.contracts.domain.model.usecases.get_all_terms_by_contract_id_usecase import GetAllTermsByContractIdUseCase
from appV2.contracts.infrastructure.dependencies.dependencies import get_get_all_terms_by_contract_id_usecase
from appV2.profiles.application.exceptions.profile_exceptions import ProfileNotFoundError

@router.get(
    '/{contract_id}/terms',
    summary='Get terms by contract id',
    tags=['Terms'],
    response_model=List[TermResource],
    status_code=status.HTTP_200_OK,
    responses={
        TokenNotFoundError().status_code: TokenNotFoundError().get_response_model(),
        TokenExpiredError().status_code: TokenExpiredError().get_response_model(),
        TokenInvalidError().status_code: TokenInvalidError().get_response_model(),
        ProfileNotFoundError().status_code: ProfileNotFoundError().get_response_model(),
        ContractNotFoundError().status_code: ContractNotFoundError().get_response_model(),
    },
)
def get_all_terms_by_contract_id(
    response: Response,
    request: Request,
    contract_id: int,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    get_all_terms_by_contract_id_usecase: GetAllTermsByContractIdUseCase = Depends(get_get_all_terms_by_contract_id_usecase),
):
    contracts = get_all_terms_by_contract_id_usecase((token, contract_id))
    return contracts