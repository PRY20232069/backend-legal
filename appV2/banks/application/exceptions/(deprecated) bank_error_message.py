from pydantic import BaseModel, Field

from appV2.banks.application.exceptions.bank_exceptions import (
    BankNotFoundError,
    BankAlreadyExistsError
)


class ErrorMessageBankNotFound(BaseModel):
    detail: str = Field(example=BankNotFoundError.message)


class ErrorMessageBankAlreadyExists(BaseModel):
    detail: str = Field(example=BankAlreadyExistsError.message)
