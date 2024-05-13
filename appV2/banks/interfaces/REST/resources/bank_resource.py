from pydantic import BaseModel, Field

from appV2.banks.domain.model.entities.bank import Bank

class BankResource(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example='BCP')

    @staticmethod
    def from_entity(entity: Bank) -> 'BankResource':
        return BankResource(
            id=entity.id,
            name=entity.name
        )