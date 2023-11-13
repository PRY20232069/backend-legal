from pydantic import BaseModel

class TermResource(BaseModel):
    id: int
    description: str
    interpretation: str | None
    consumer_protection_law: str | None
    index: int
    num_page: int
    contract_id: int