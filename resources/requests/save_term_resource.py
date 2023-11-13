from pydantic import BaseModel

from models.term import Term

class SaveTermResource(BaseModel):
    description: str
    index: int
    num_page: int

    def to_model(self, contract_id: int) -> Term:
        return Term(
            description=self.description,
            index=self.index,
            num_page=self.num_page,
            contract_id=contract_id,
        )