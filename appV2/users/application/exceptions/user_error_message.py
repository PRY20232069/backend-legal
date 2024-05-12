from pydantic import BaseModel, Field

from appV2.users.application.exceptions.user_exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError
)


class ErrorMessageUserNotFound(BaseModel):
    detail: str = Field(example=UserNotFoundError.message)


class ErrorMessageUserAlreadyExists(BaseModel):
    detail: str = Field(example=UserAlreadyExistsError.message)
