from fastapi import Depends, HTTPException, status, Response, Request, UploadFile, File
from fastapi.security import HTTPBearer

from typing import Tuple

from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError
from appV2._shared.application.exceptions.app_error_message import ErrorMessageTokenNotFound
from appV2.contracts.interfaces.REST.controllers.contracts_controller import router
from appV2.contracts.interfaces.REST.resources.save_contract_resource import SaveContractResource
from appV2.contracts.interfaces.REST.resources.contract_resource import ContractResource
from appV2.contracts.domain.model.usecases.upload_contract_usecase import UploadContractUseCase
from appV2.contracts.infrastructure.dependencies.dependencies import get_upload_contract_usecase
from appV2.contracts.application.exceptions.contract_exceptions import ContractAlreadyExistsError
from appV2.contracts.application.exceptions.contract_error_message import ErrorMessageContractAlreadyExists

@router.post(
    '/',
    summary='Create a new contract',
    response_model=ContractResource,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            'model': ErrorMessageTokenNotFound
        },
        status.HTTP_409_CONFLICT: {
            'model': ErrorMessageContractAlreadyExists
        }
    },
)
def upload_contract(
    data: SaveContractResource,
    response: Response,
    request: Request,
    # contract_file: UploadFile = File(...),
    token: str = Depends(HTTPBearer()),
    upload_contract_usecase: UploadContractUseCase = Depends(get_upload_contract_usecase),
):
    try:
        contract = upload_contract_usecase((token, data))
    except TokenNotFoundError as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exception.message
        )
    except ContractAlreadyExistsError as exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exception.message
        )
    except Exception as _exception:
        print(_exception)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return contract