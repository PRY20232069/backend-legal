from appV2._shared.application.exceptions.base_exceptions import BaseNotFoundError, BaseConflictError, BaseBadRequestError


class ProfileNotFoundError(BaseNotFoundError):
    message = 'Profile does not exist.'


class ProfileAlreadyExistsError(BaseConflictError):
    message = 'Profile already exists'


class CreateProfileError(BaseBadRequestError):
    message = 'An error occurred while creating the profile'

    
class UpdateProfileError(BaseBadRequestError):
    message = 'An error occurred while updating the profile'