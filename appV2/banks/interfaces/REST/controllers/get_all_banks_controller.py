from typing import List
from fastapi import Depends, HTTPException, status, Response, Request, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError, TokenExpiredError, TokenInvalidError
from appV2.banks.interfaces.REST.controllers.banks_controller import router
from appV2.banks.interfaces.REST.resources.bank_resource import BankResource
from appV2.banks.domain.model.usecases.get_all_banks_usecase import GetAllBanksUseCase
from appV2.banks.infrastructure.dependencies.dependencies import get_get_all_banks_usecase

@router.get(
    '/all',
    summary='Get all banks',
    response_model=List[BankResource],
    status_code=status.HTTP_200_OK,
    responses={
        TokenNotFoundError().status_code: TokenNotFoundError().get_response_model(),
        TokenExpiredError().status_code: TokenExpiredError().get_response_model(),
        TokenInvalidError().status_code: TokenInvalidError().get_response_model(),
    },
)
def get_all_banks(
    response: Response,
    request: Request,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    get_all_banks_usecase: GetAllBanksUseCase = Depends(get_get_all_banks_usecase),
):
    banks = get_all_banks_usecase((token, ))
    return banks