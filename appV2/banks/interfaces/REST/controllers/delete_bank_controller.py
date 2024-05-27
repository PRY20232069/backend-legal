from typing import Tuple
from fastapi import Depends, HTTPException, status, Response, Request, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError, TokenExpiredError, TokenInvalidError
from appV2.banks.interfaces.REST.controllers.banks_controller import router
from appV2.banks.interfaces.REST.resources.bank_resource import BankResource
from appV2.banks.domain.model.usecases.delete_bank_usecase import DeleteBankUseCase
from appV2.banks.infrastructure.dependencies.dependencies import get_delete_bank_usecase
from appV2.banks.application.exceptions.bank_exceptions import BankNotFoundError, DeleteBankError, DeleteBankWithContractsError

@router.delete(
    '/{bank_id}',
    summary='Delete a bank',
    response_model=BankResource,
    status_code=status.HTTP_200_OK,
    responses={
        TokenNotFoundError().status_code: TokenNotFoundError().get_response_model(),
        TokenExpiredError().status_code: TokenExpiredError().get_response_model(),
        TokenInvalidError().status_code: TokenInvalidError().get_response_model(),
        BankNotFoundError().status_code: BankNotFoundError().get_response_model(),
        DeleteBankError().status_code: DeleteBankError().get_response_model_array([
            DeleteBankWithContractsError().message,
        ]),
    },
)
def delete_bank(
    response: Response,
    request: Request,
    bank_id: int,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    delete_bank_usecase: DeleteBankUseCase = Depends(get_delete_bank_usecase),
):
    bank = delete_bank_usecase((token, bank_id))
    return bank