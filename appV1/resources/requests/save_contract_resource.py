from pydantic import BaseModel

from appV1.models.contract import Contract

class SaveContractResource(BaseModel):
    name: str
    bank_id: int
    favorite: bool = False

    def to_model(self, profile_id: int) -> Contract:
        return Contract(
            name=self.name,
            favorite=self.favorite,
            profile_id=profile_id,
            bank_id=self.bank_id,
        )