from pydantic import BaseModel, Field

from appV2.banks.domain.model.entities.bank import Bank

class BankResource(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example='BCP')
    logo_url: str = Field(example='https://bcp_logo.com.png')
    contracts_count: int = Field(example=0)

    @staticmethod
    def from_entity(entity: Bank) -> 'BankResource':
        return BankResource(
            id=entity.id,
            name=entity.name,
            logo_url=entity.logo_url,
            contracts_count=0
        )