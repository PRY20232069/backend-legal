from pydantic import BaseModel, Field

from appV2.contracts.domain.model.entities.term import Term

class TermResource(BaseModel):
    id: int = Field(example=1)
    description: str = Field(example='Term description')
    interpretation: str | None = Field(example='Interpretation')
    consumer_protection_law: str | None = Field(example='Consumer Protection Law')
    abusive: bool = Field(example=False)
    contract_id: int = Field(example=1)

    @staticmethod
    def from_entity(entity: Term) -> 'TermResource':
        return TermResource(
            id=entity.id,
            description=entity.description,
            interpretation=entity.interpretation,
            consumer_protection_law=entity.consumer_protection_law,
            abusive=entity.abusive,
            contract_id=entity.contract_id,
        )