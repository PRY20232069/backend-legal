from typing import Tuple
from fastapi import Depends, HTTPException, status, Response, Request, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError, TokenExpiredError, TokenInvalidError
from appV2.banks.interfaces.REST.controllers.banks_controller import router
from appV2.banks.interfaces.REST.resources.save_bank_resource import SaveBankResource
from appV2.banks.interfaces.REST.resources.bank_resource import BankResource
from appV2.banks.domain.model.usecases.update_bank_usecase import UpdateBankUseCase
from appV2.banks.infrastructure.dependencies.dependencies import get_update_bank_usecase
from appV2.banks.application.exceptions.bank_exceptions import BankNotFoundError, UpdateBankError

@router.put(
    '/{bank_id}',
    summary='Update a bank',
    response_model=BankResource,
    status_code=status.HTTP_200_OK,
    responses={
        TokenNotFoundError().status_code: TokenNotFoundError().get_response_model(),
        TokenExpiredError().status_code: TokenExpiredError().get_response_model(),
        TokenInvalidError().status_code: TokenInvalidError().get_response_model(),
        BankNotFoundError().status_code: BankNotFoundError().get_response_model(),
        UpdateBankError().status_code: UpdateBankError().get_response_model(),
    },
)
def update_bank(
    data: SaveBankResource,
    response: Response,
    request: Request,
    bank_id: int,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    update_bank_usecase: UpdateBankUseCase = Depends(get_update_bank_usecase),
):
    bank = update_bank_usecase(((token, bank_id), data))
    return bank