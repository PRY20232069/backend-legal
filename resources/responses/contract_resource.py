from datetime import datetime
from pydantic import BaseModel


class ContractResource(BaseModel):
    id: int
    name: str
    favorite: bool
    uploaded_date: datetime
    profile_id: int
    bank_id: int

    def __init__(self, id: int, name: str, favorite: bool, uploaded_date: datetime, profile_id: int, bank_id: int):
        super().__init__(id=id, name=name, favorite=favorite, uploaded_date=uploaded_date, profile_id=profile_id, bank_id=bank_id)