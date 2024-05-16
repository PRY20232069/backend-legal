from typing import Tuple
from fastapi import Depends, HTTPException, status, Response, Request, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError, TokenExpiredError, TokenInvalidError
from appV2.banks.interfaces.REST.controllers.banks_controller import router
from appV2.banks.interfaces.REST.resources.save_bank_resource import SaveBankResource
from appV2.banks.interfaces.REST.resources.bank_resource import BankResource
from appV2.banks.domain.model.usecases.create_bank_usecase import CreateBankUseCase
from appV2.banks.infrastructure.dependencies.dependencies import get_create_bank_usecase
from appV2.banks.application.exceptions.bank_exceptions import BankAlreadyExistsError, CreateBankError

@router.post(
    '',
    summary='Create a new bank',
    response_model=BankResource,
    status_code=status.HTTP_201_CREATED,
    responses={
        TokenNotFoundError().status_code: TokenNotFoundError().get_response_model(),
        TokenExpiredError().status_code: TokenExpiredError().get_response_model(),
        TokenInvalidError().status_code: TokenInvalidError().get_response_model(),
        BankAlreadyExistsError().status_code: BankAlreadyExistsError().get_response_model(),
        CreateBankError().status_code: CreateBankError().get_response_model(),
    },
)
def create_bank(
    data: SaveBankResource,
    response: Response,
    request: Request,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    create_bank_usecase: CreateBankUseCase = Depends(get_create_bank_usecase),
):
    bank = create_bank_usecase((token, data))
    return bank