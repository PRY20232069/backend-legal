from fastapi import Depends, HTTPException, status, Response, Request, APIRouter
from fastapi.security import HTTPBearer

from typing import List

from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError
from appV2._shared.application.exceptions.app_error_message import ErrorMessageTokenNotFound
from appV2.contracts.interfaces.REST.controllers.contracts_controller import router
from appV2.contracts.interfaces.REST.resources.contract_resource import ContractResource
from appV2.contracts.domain.model.usecases.get_all_contracts_usecase import GetAllContractsUseCase
from appV2.contracts.infrastructure.dependencies.dependencies import get_get_all_contracts_by_user_id_usecase

@router.get(
    '/all',
    summary='Get all contracts',
    response_model=List[ContractResource],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            'model': ErrorMessageTokenNotFound
        },
    },
)
def get_all_contracts(
    response: Response,
    request: Request,
    token: str = Depends(HTTPBearer()),
    get_all_contracts_usecase: GetAllContractsUseCase = Depends(get_get_all_contracts_by_user_id_usecase),
):
    try:
        contracts = get_all_contracts_usecase((token, ))
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

    return contracts