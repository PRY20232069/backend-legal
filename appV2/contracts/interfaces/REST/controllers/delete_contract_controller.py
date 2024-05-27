from typing import Tuple
from fastapi import Depends, HTTPException, status, Response, Request, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError, TokenExpiredError, TokenInvalidError
from appV2.contracts.interfaces.REST.controllers.contracts_controller import router
from appV2.contracts.interfaces.REST.resources.contract_resource import ContractResource
from appV2.contracts.domain.model.usecases.delete_contract_usecase import DeleteContractUseCase
from appV2.contracts.infrastructure.dependencies.dependencies import get_delete_contract_usecase
from appV2.contracts.application.exceptions.contract_exceptions import ContractNotFoundError, DeleteContractError
from appV2.banks.application.exceptions.bank_exceptions import BankNotFoundError
from appV2.profiles.application.exceptions.profile_exceptions import ProfileNotFoundError

@router.delete(
    '/{contract_id}',
    summary='Delete a contract',
    response_model=ContractResource,
    status_code=status.HTTP_200_OK,
    responses={
        TokenNotFoundError().status_code: TokenNotFoundError().get_response_model(),
        TokenExpiredError().status_code: TokenExpiredError().get_response_model(),
        TokenInvalidError().status_code: TokenInvalidError().get_response_model(),
        ProfileNotFoundError().status_code: ProfileNotFoundError().get_response_model_array([
            BankNotFoundError().message,
            ContractNotFoundError().message]),
        DeleteContractError().status_code: DeleteContractError().get_response_model(),
    },
)
def delete_contract(
    response: Response,
    request: Request,
    contract_id: int,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    delete_contract_usecase: DeleteContractUseCase = Depends(get_delete_contract_usecase),
):
    contract = delete_contract_usecase((token, contract_id))
    return contract