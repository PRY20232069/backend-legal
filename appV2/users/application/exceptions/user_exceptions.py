from appV2._shared.application.exceptions.base_exceptions import BaseNotFoundError, BaseConflictError, BaseUnauthorizedError, BaseBadRequestError


class UserNotFoundError(BaseNotFoundError):
    message = 'User does not exist.'


class UserAlreadyExistsError(BaseConflictError):
    message = 'User already exists'


class UserInvalidCredentialsError(BaseUnauthorizedError):
    message = 'Invalid credentials.'
    
    
class RegisterUserError(BaseBadRequestError):
    message = 'An error occurred while registering the user.'

    
class RecoverUserError(BaseBadRequestError):
    message = 'An error occurred while recovering the user.'