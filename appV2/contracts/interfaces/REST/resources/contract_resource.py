from datetime import datetime
from pydantic import BaseModel, Field

from appV2.contracts.domain.model.entities.contract import Contract

class ContractResource(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example='Contract_Name.pdf')
    favorite: bool = Field(example=False)
    file_url: str | None = Field(example='https://google.com')
    uploaded_date: datetime = Field(example=datetime.now())
    profile_id: int = Field(example=1)
    bank_id: int = Field(example=1)

    @staticmethod
    def from_entity(entity: Contract) -> 'ContractResource':
        return ContractResource(
            id=entity.id,
            name=entity.name,
            favorite=entity.favorite,
            file_url=entity.file_url,
            uploaded_date=entity.uploaded_date,
            profile_id=entity.profile_id,
            bank_id=entity.bank_id,
        )