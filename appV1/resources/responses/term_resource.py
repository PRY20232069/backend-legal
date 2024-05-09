from pydantic import BaseModel

class TermResource(BaseModel):
    id: int | None
    description: str
    interpretation: str | None
    consumer_protection_law: str | None
    index: int
    num_page: int | None
    contract_id: int | None