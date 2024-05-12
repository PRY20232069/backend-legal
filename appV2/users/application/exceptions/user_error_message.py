from pydantic import BaseModel, Field

from appV2.users.application.exceptions.user_exceptions import (
    UserNotFoundError,
    UsersNotFoundError,
    UserAlreadyExistsError
)


class ErrorMessageUserNotFound(BaseModel):
    detail: str = Field(example=UserNotFoundError.message)


class ErrorMessageUsersNotFound(BaseModel):
    detail: str = Field(example=UsersNotFoundError.message)


class ErrorMessageUserAlreadyExists(BaseModel):
    detail: str = Field(example=UserAlreadyExistsError.message)
