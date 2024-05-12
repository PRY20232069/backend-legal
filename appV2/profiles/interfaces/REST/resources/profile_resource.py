from pydantic import BaseModel, Field
from datetime import datetime

from appV2.profiles.domain.model.entities.profile import Profile

class ProfileResource(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example='Juan')
    last_name: str = Field(example='Perez')
    birth_date: datetime = Field(example='1990-01-01T00:00:00')
    district: str = Field(example='San Francisco')
    region: str = Field(example='California')
    created_at: datetime = Field(example='2022-01-01')
    user_id: int = Field(example=1)
    
    @staticmethod
    def from_entity(entity: Profile) -> 'ProfileResource':
        return ProfileResource(
            id=entity.id,
            name=entity.name,
            last_name=entity.last_name,
            birth_date=entity.birth_date,
            district=entity.district,
            region=entity.region,
            created_at=entity.created_at,
            user_id=entity.user_id
        )