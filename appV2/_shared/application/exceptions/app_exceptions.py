from appV2._shared.application.exceptions.base_exceptions import BaseForbiddenError, BaseUnauthorizedError, BaseUnprocessableEntityError


class TokenInvalidError(BaseUnprocessableEntityError):
    message = 'Invalid token'


class TokenNotFoundError(BaseForbiddenError):
    message = {
        'detail': 'Not authenticated'
    }


class TokenExpiredError(BaseUnauthorizedError):
    message = 'Token expired'