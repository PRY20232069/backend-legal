from pydantic import BaseModel

class BankResource(BaseModel):
    id: int
    name: str