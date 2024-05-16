from appV2._shared.application.exceptions.base_exceptions import BaseBadRequestError


class CreateTermError(BaseBadRequestError):
    message = 'An error occurred while creating a term'