from fastapi import Depends, HTTPException, status, Response, Request, APIRouter
from fastapi.security import HTTPBearer

from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError
from appV2._shared.application.exceptions.app_error_message import ErrorMessageTokenNotFound
from appV2.contracts.interfaces.REST.controllers.contracts_controller import router
from appV2.contracts.interfaces.REST.resources.contract_resource import ContractResource
from appV2.contracts.domain.model.usecases.get_contract_by_id_usecase import GetContractByIdUseCase
from appV2.contracts.infrastructure.dependencies.dependencies import get_get_contract_by_id_usecase
from appV2.contracts.application.exceptions.contract_exceptions import ContractNotFoundError
from appV2.contracts.application.exceptions.contract_error_message import ErrorMessageContractNotFound

@router.get(
    '/{contract_id}',
    summary='Get contract by id',
    response_model=ContractResource,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            'model': ErrorMessageTokenNotFound
        },
        status.HTTP_404_NOT_FOUND: {
            'model': ErrorMessageContractNotFound
        },
    },
)
def get_contract_by_id(
    response: Response,
    request: Request,
    contract_id: int,
    token: str = Depends(HTTPBearer()),
    get_contract_by_id_usecase: GetContractByIdUseCase = Depends(get_get_contract_by_id_usecase),
):
    try:
        contract = get_contract_by_id_usecase((token, contract_id))
    except TokenNotFoundError as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exception.message
        )
    except ContractNotFoundError as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exception.message
        )
    except Exception as _exception:
        print(_exception)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return contract