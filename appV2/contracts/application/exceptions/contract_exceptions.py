from appV2._shared.application.exceptions.base_exception import BaseError


class ContractNotFoundError(BaseError):
    message = 'Contract does not exist.'


class ContractAlreadyExistsError(BaseError):
    message = 'Contract already exists'