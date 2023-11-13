from pydantic import BaseModel

class UserResource(BaseModel):
    id: int
    email: str