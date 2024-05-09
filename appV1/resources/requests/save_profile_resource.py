from datetime import datetime
from pydantic import BaseModel

from appV1.models.profile import Profile


class SaveProfileResource(BaseModel):
    name: str
    last_name: str
    birth_date: datetime
    district: str
    region: str

    def to_model(self, user_id: int) -> Profile:
        return Profile(
            name=self.name,
            last_name=self.last_name,
            birth_date=self.birth_date,
            district=self.district,
            region=self.region,
            user_id=user_id,
        )