from datetime import datetime
from pydantic import BaseModel


class ProfileResource(BaseModel):
    id: int
    name: str
    last_name: str
    birth_date: datetime
    district: str
    region: str
    created_at: datetime
    user_id: int