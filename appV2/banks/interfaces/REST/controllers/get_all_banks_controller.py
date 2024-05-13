from fastapi import Depends, HTTPException, status, Response, Request, APIRouter
from fastapi.security import HTTPBearer

from typing import List

from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError
from appV2._shared.application.exceptions.app_error_message import ErrorMessageTokenNotFound
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
        status.HTTP_401_UNAUTHORIZED: {
            'model': ErrorMessageTokenNotFound
        },
    },
)
def get_all_banks(
    response: Response,
    request: Request,
    token: str = Depends(HTTPBearer()),
    get_all_banks_usecase: GetAllBanksUseCase = Depends(get_get_all_banks_usecase),
):
    try:
        banks = get_all_banks_usecase((token, ))
    except TokenNotFoundError as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exception.message
        )
    except Exception as _exception:
        print(_exception)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return banks