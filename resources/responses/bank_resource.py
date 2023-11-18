from pydantic import BaseModel

class BankResource(BaseModel):
    id: int
    name: str
    contracts_count: int | None = 0