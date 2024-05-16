from typing import Tuple
from fastapi import Depends, HTTPException, status, Response, Request, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from appV2._shared.application.exceptions.app_exceptions import TokenNotFoundError, TokenExpiredError, TokenInvalidError
from appV2.contracts.interfaces.REST.controllers.contracts_controller import router
from appV2.contracts.interfaces.REST.resources.contract_resource import ContractResource
from appV2.contracts.domain.model.usecases.upload_contract_usecase import UploadContractUseCase
from appV2.contracts.infrastructure.dependencies.dependencies import get_upload_contract_usecase
from appV2.contracts.application.exceptions.contract_exceptions import ContractAlreadyExistsError, UploadContractError
from appV2.contracts.application.exceptions.term_exceptions import CreateTermError
from appV2.profiles.application.exceptions.profile_exceptions import ProfileNotFoundError
from appV2.banks.application.exceptions.bank_exceptions import BankNotFoundError

@router.post(
    '/banks/{bank_id}',
    summary='Upload a new contract',
    response_model=ContractResource,
    status_code=status.HTTP_201_CREATED,
    responses={
        TokenNotFoundError().status_code: TokenNotFoundError().get_response_model(),
        TokenExpiredError().status_code: TokenExpiredError().get_response_model(),
        TokenInvalidError().status_code: TokenInvalidError().get_response_model(),
        ProfileNotFoundError().status_code: ProfileNotFoundError().get_response_model_array([
            BankNotFoundError().message]),
        ContractAlreadyExistsError().status_code: ContractAlreadyExistsError().get_response_model(),
        UploadContractError().status_code: UploadContractError().get_response_model_array([
            CreateTermError().message]),
    },
)
async def upload_contract(
    response: Response,
    request: Request,
    bank_id: int,
    contract_file: UploadFile = File(...),
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    upload_contract_usecase: UploadContractUseCase = Depends(get_upload_contract_usecase),
):
    contract = await upload_contract_usecase(((token, bank_id), contract_file))
    return contract