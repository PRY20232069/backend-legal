from appV2._shared.application.exceptions.base_exception import BaseError


class InvalidCredentialsError(BaseError):
    message = 'Invalid credentials.'


class TokenNotFoundError(BaseError):
    message = 'Token not found.'


class TokenExpiredError(BaseError):
    message = 'Token expired.'