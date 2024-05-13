from appV2._shared.application.exceptions.base_exception import BaseError


class BankNotFoundError(BaseError):
    message = 'Bank does not exist.'


class BankAlreadyExistsError(BaseError):
    message = 'Bank already exists'