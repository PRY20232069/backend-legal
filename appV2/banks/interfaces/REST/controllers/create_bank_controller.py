from fastapi import Depends, HTTPException, status, Response, Request, APIRouter
from fastapi.security import HTTPBearer

from typing import Tuple

from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError
from appV2._shared.application.exceptions.app_error_message import ErrorMessageTokenNotFound
from appV2.banks.interfaces.REST.controllers.banks_controller import router
from appV2.banks.interfaces.REST.resources.save_bank_resource import SaveBankResource
from appV2.banks.interfaces.REST.resources.bank_resource import BankResource
from appV2.banks.domain.model.usecases.create_bank_usecase import CreateBankUseCase
from appV2.banks.infrastructure.dependencies.dependencies import get_create_bank_usecase
from appV2.banks.application.exceptions.bank_exceptions import BankAlreadyExistsError
from appV2.banks.application.exceptions.bank_error_message import ErrorMessageBankAlreadyExists

@router.post(
    '/',
    summary='Create a new bank',
    response_model=BankResource,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            'model': ErrorMessageTokenNotFound
        },
        status.HTTP_409_CONFLICT: {
            'model': ErrorMessageBankAlreadyExists
        }
    },
)
def create_bank(
    data: SaveBankResource,
    response: Response,
    request: Request,
    token: str = Depends(HTTPBearer()),
    create_bank_usecase: CreateBankUseCase = Depends(get_create_bank_usecase),
):
    try:
        bank = create_bank_usecase((token, data))
    except TokenNotFoundError as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exception.message
        )
    except BankAlreadyExistsError as exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exception.message
        )
    except Exception as _exception:
        print(_exception)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return bank