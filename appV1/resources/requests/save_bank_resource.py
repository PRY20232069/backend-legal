from pydantic import BaseModel

from appV1.models.bank import Bank

class SaveBankResource(BaseModel):
    name: str

    def to_model(self) -> Bank:
        return Bank(
            name=self.name,
        )