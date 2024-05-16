from fastapi import Depends, HTTPException, status, Response, Request, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError, TokenExpiredError, TokenInvalidError
from appV2.contracts.interfaces.REST.controllers.contracts_controller import router
from appV2.contracts.interfaces.REST.resources.contract_resource import ContractResource
from appV2.contracts.domain.model.usecases.get_contract_by_id_usecase import GetContractByIdUseCase
from appV2.contracts.infrastructure.dependencies.dependencies import get_get_contract_by_id_usecase
from appV2.contracts.application.exceptions.contract_exceptions import ContractNotFoundError
from appV2.profiles.application.exceptions.profile_exceptions import ProfileNotFoundError

@router.get(
    '/{contract_id}',
    summary='Get contract by id',
    response_model=ContractResource,
    status_code=status.HTTP_200_OK,
    responses={
        TokenNotFoundError().status_code: TokenNotFoundError().get_response_model(),
        TokenExpiredError().status_code: TokenExpiredError().get_response_model(),
        TokenInvalidError().status_code: TokenInvalidError().get_response_model(),
        ProfileNotFoundError().status_code: ProfileNotFoundError().get_response_model(),
        ContractNotFoundError().status_code: ContractNotFoundError().get_response_model(),
    },
)
def get_contract_by_id(
    response: Response,
    request: Request,
    contract_id: int,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    get_contract_by_id_usecase: GetContractByIdUseCase = Depends(get_get_contract_by_id_usecase),
):
    contract = get_contract_by_id_usecase((token, contract_id))
    return contract