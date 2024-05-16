from typing import List
from fastapi import Depends, HTTPException, status, Response, Request, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError, TokenExpiredError, TokenInvalidError
from appV2.contracts.interfaces.REST.controllers.contracts_controller import router
from appV2.contracts.interfaces.REST.resources.contract_resource import ContractResource
from appV2.contracts.domain.model.usecases.get_all_contracts_usecase import GetAllContractsUseCase
from appV2.contracts.infrastructure.dependencies.dependencies import get_get_all_contracts_by_user_id_usecase
from appV2.profiles.application.exceptions.profile_exceptions import ProfileNotFoundError

@router.get(
    '/all',
    summary='Get all contracts',
    response_model=List[ContractResource],
    status_code=status.HTTP_200_OK,
    responses={
        TokenNotFoundError().status_code: TokenNotFoundError().get_response_model(),
        TokenExpiredError().status_code: TokenExpiredError().get_response_model(),
        TokenInvalidError().status_code: TokenInvalidError().get_response_model(),
        ProfileNotFoundError().status_code: ProfileNotFoundError().get_response_model(),
    },
)
def get_all_contracts(
    response: Response,
    request: Request,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    get_all_contracts_usecase: GetAllContractsUseCase = Depends(get_get_all_contracts_by_user_id_usecase),
):
    contracts = get_all_contracts_usecase((token, ))
    return contracts