from pydantic import BaseModel, Field

from appV2._shared.application.exceptions.app_exceptions import (
    InvalidCredentialsError,
    TokenNotFoundError,
    TokenExpiredError
)

class ErrorMessageInvalidCredentials(BaseModel):
    detail: str = Field(example=InvalidCredentialsError.message)


class ErrorMessageTokenNotFound(BaseModel):
    detail: str = Field(example=TokenNotFoundError.message)


class ErrorMessageTokenExpired(BaseModel):
    detail: str = Field(example=TokenExpiredError.message)