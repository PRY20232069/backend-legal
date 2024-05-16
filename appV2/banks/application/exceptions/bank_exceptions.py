from appV2._shared.application.exceptions.base_exceptions import BaseError, BaseBadRequestError, BaseNotFoundError, BaseConflictError


class BankNotFoundError(BaseNotFoundError):
    message = 'Bank does not exist.'


class BankAlreadyExistsError(BaseConflictError):
    message = 'Bank already exists'


class CreateBankError(BaseBadRequestError):
    message = 'An error occurred while creating the bank'