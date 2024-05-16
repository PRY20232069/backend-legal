from pydantic import BaseModel, Field

from appV2.profiles.application.exceptions.profile_exceptions import (
    ProfileNotFoundError,
    ProfileAlreadyExistsError
)


class ErrorMessageProfileNotFound(BaseModel):
    detail: str = Field(example=ProfileNotFoundError.message)


class ErrorMessageProfileAlreadyExists(BaseModel):
    detail: str = Field(example=ProfileAlreadyExistsError.message)
