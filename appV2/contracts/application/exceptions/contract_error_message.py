from pydantic import BaseModel, Field

from appV2.contracts.application.exceptions.contract_exceptions import (
    ContractNotFoundError,
    ContractAlreadyExistsError
)


class ErrorMessageContractNotFound(BaseModel):
    detail: str = Field(example=ContractNotFoundError.message)


class ErrorMessageContractAlreadyExists(BaseModel):
    detail: str = Field(example=ContractAlreadyExistsError.message)
