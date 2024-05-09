from appV2._shared.application.exceptions.base_exception import BaseError


class UserNotFoundError(BaseError):
    message = 'User does not exist.'


class UsersNotFoundError(BaseError):
    message = 'Users do not exist'


class UserAlreadyExistsError(BaseError):
    message = 'User already exists'