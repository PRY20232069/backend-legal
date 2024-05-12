from appV2._shared.application.exceptions.base_exception import BaseError


class ProfileNotFoundError(BaseError):
    message = 'Profile does not exist.'


class ProfileAlreadyExistsError(BaseError):
    message = 'Profile already exists'