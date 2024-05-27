from appV2._shared.application.exceptions.base_exceptions import BaseError, BaseBadRequestError, BaseNotFoundError, BaseConflictError


class ContractNotFoundError(BaseNotFoundError):
    message = 'Contract does not exist.'


class ContractAlreadyExistsError(BaseConflictError):
    message = 'Contract already exists'


class UploadContractError(BaseBadRequestError):
    message = 'An error occurred while uploading the contract'

    
class UpdateContractError(BaseBadRequestError):
    message = 'An error occurred while updating the contract'

    
class DeleteContractError(BaseBadRequestError):
    message = 'An error occurred while deleting the contract'